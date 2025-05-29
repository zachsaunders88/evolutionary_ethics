#!/usr/bin/env python
# coding: utf-8

import os
from pathlib import Path
from pyswip import Prolog
import random
import numpy as np
import sqlite3
from deap import base, creator, tools

# Compute absolute path to the .pl file
pl_path = (
    Path(__file__).parent.parent  # parent of notebooks/ is evolutionary_ethics
    / "symbolic_reasoning_sys"
    / "ethics_engine_final.pl"
).resolve()

# Convert to forward-slash string
pl_str = pl_path.as_posix()

# Debug: print repr to confirm it’s like C:/.../file.pl
print(">>> PROLOG file to consult:", repr(pl_str))

consult_cmd = f"consult('{pl_str}')."

# Initialize Prolog and load file
prolog = Prolog()
consult_cmd = f"consult('{pl_str}')."
# Use query to avoid backslash escape issues
list(prolog.query(consult_cmd))

GROUND_TRUTH = {
    'dropped_wallet_1': 'return_wallet',
    'dropped_wallet_2': 'return_wallet', 
    'dropped_wallet_3': 'return_wallet',
    'dropped_wallet_4': 'leave_wallet',
    'dropped_wallet_5': 'return_wallet',
    'dropped_wallet_6': 'take_wallet',
    'dropped_wallet_7': 'leave_wallet',
    'dropped_wallet_8': 'take_wallet',
}

def update_weights_in_file(weights):
    """
    Overwrite weight/2 facts in the Prolog file with new values.
    weights is a list or array: [w_utilitarian, w_deontological, w_self_interest]
    """
    with open(pl_path, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith("weight(utilitarian"):
            new_lines.append(f"weight(utilitarian, {weights[0]:.3f}).\n")
        elif line.strip().startswith("weight(deontological"):
            new_lines.append(f"weight(deontological, {weights[1]:.3f}).\n")
        elif line.strip().startswith("weight(self_interest"):
            new_lines.append(f"weight(self_interest, {weights[2]:.3f}).\n")
        else:
            new_lines.append(line)

    with open(pl_path, "w") as f:
        f.writelines(new_lines)

def run_prolog_query(weights):
    """
    Given a weight vector, update Prolog file, reload Prolog engine,
    run make_decision for all scenarios and calculate accuracy.
    """
    weights = np.array(weights)
    weights = weights / np.sum(weights)  # Normalize weights to sum to 1

    update_weights_in_file(weights)

    prolog = Prolog()
    consult_cmd = f"consult('{pl_str}')."
    list(prolog.query(consult_cmd))

    correct = 0
    total = len(GROUND_TRUTH)

    for scenario_name, true_action in GROUND_TRUTH.items():
        query = f"make_decision({scenario_name}, Action, Justification, Score)."
        results = list(prolog.query(query))
        if not results:
            continue
        predicted = results[0]["Action"]
        if predicted == true_action:
            correct += 1

    accuracy = correct / total
    return (accuracy,)

if __name__ == "__main__":
    test_weights = [0.33, 0.33, 0.34]
    acc = run_prolog_query(test_weights)[0]
    print(f"Accuracy for weights {test_weights}: {acc:.2f}")

scenario_data = [
    ("dropped_wallet_1", ("dropped_wallet", True, True, "many_people_around")),
    ("dropped_wallet_2", ("dropped_wallet", True, True, "isolated_area")),
    ("dropped_wallet_3", ("dropped_wallet", True, False, "many_people_around")),
    ("dropped_wallet_4", ("dropped_wallet", True, False, "isolated_area")),
    ("dropped_wallet_5", ("dropped_wallet", False, True, "many_people_around")),
    ("dropped_wallet_6", ("dropped_wallet", False, True, "isolated_area")),
    ("dropped_wallet_7", ("dropped_wallet", False, False, "many_people_around")),
    ("dropped_wallet_8", ("dropped_wallet", False, False, "isolated_area")),
]

all_scenarios = {name: (event, (owner_nearby, contents_valuable, environment))
                 for name, (event, owner_nearby, contents_valuable, environment) in scenario_data}

def predict_action(scenario_name, weights):
    update_weights_in_file(weights)
    result = list(prolog.query(f"make_decision({scenario_name}, Action, Justification, Score)"))
    if result:
        return result[0]['Action'], result[0]['Justification'], result[0]['Score']
    else:
        return None, None, None

# === DEAP SETUP ===

if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_float", random.uniform, 0, 1)  # Individuals are 3 floating-point numbers between 0 and 1
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators
toolbox.register("evaluate", run_prolog_query)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.5)
toolbox.register("select", tools.selTournament, tournsize=3)

def main():
    random.seed(42)
    population = toolbox.population(n=50)
    NGEN = 20
    CXPB = 0.5  # crossover probability
    MUTPB = 0.3  # mutation probability

    print("Start of evolution")
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    for gen in range(1, NGEN + 1):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate invalid fitnesses
        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring

        top = tools.selBest(population, 1)[0]
        normalized_weights = np.round(np.array(top) / np.sum(top), 3)
        print(f"Gen {gen}: Best Accuracy = {top.fitness.values[0]:.2f} | Weights = {normalized_weights}")

    best_ind = tools.selBest(population, 1)[0]
    final_decisions = []
    for scenario in all_scenarios:
        action = predict_action(scenario, best_ind)
        rules = list(prolog.query(f"rule_sources({scenario}, {action}, Sources)."))
        print(f"Scenario: {scenario}, Action: {action}, Rules: {rules}")

        # action might be a tuple (Action, Justification, Score)
        if isinstance(action, tuple) and len(action) == 3:
            action_val, justification, score = action
        else:
            action_val, justification, score = action, None, None

        final_decisions.append((
            scenario,
            action_val,
            justification,
            score
        ))
            
    return final_decisions

if __name__ == "__main__":
    main()

print(run_prolog_query([0.8, 0.1, 0.1]))  # Mostly utilitarian
print(run_prolog_query([0.1, 0.8, 0.1]))  # Mostly deontological
print(run_prolog_query([0.1, 0.1, 0.8]))  # Mostly self-interest

#!/usr/bin/env python
# coding: utf-8

import os

# Linux environment retained, not applicable to Windows
# os.environ["SWI_HOME_DIR"] = os.path.expanduser("~/.local/swipl/lib/swipl")
# os.environ["LD_LIBRARY_PATH"] = os.path.expanduser("~/.local/swipl/lib/swipl/lib/x86_64-linux")
# os.environ["PATH"] = os.path.expanduser("~/.local/swipl/bin") + ":" + os.environ["PATH"]

from pyswip import Prolog
from pathlib import Path
from deap import base, creator, tools, algorithms
import numpy as np
import deap
import random

# Step 1: Start from the directory of the current script (notebooks)
HERE = Path(__file__).parent

# Step 2: Go back to the project root: notebooks -> evolutionary_ethics -> ETHICS_INTERFACE
PROJECT_ROOT = HERE.parent

# Step 3: Build the path to the Prolog file (retain the "expanded versions" space)
base_dir = PROJECT_ROOT / "symbolic_reasoning_sys" / "expanded versions"

# Step 4: Final .pl file
PROLOG_FILE = base_dir / "ethics_engine_expanded_32.pl"
prolog = Prolog()
pl_str = PROLOG_FILE.as_posix()
consult_cmd = f"consult('{pl_str}')."
list(prolog.query(consult_cmd))

# GROUND TRUTH
GROUND_TRUTH = {
    "dropped_wallet_1": "return_wallet",
    "dropped_wallet_2": "return_wallet",
    "dropped_wallet_3": "return_wallet",
    "dropped_wallet_4": "return_wallet",
    "dropped_wallet_5": "return_wallet",
    "dropped_wallet_6": "return_wallet",
    "dropped_wallet_7": "return_wallet",
    "dropped_wallet_8": "return_wallet",
    "dropped_wallet_9": "return_wallet",
    "dropped_wallet_10": "return_wallet",
    "dropped_wallet_11": "return_wallet",
    "dropped_wallet_12": "return_wallet",
    "dropped_wallet_13": "return_wallet",
    "dropped_wallet_14": "return_wallet",
    "dropped_wallet_15": "return_wallet",
    "dropped_wallet_16": "return_wallet",
    "dropped_wallet_17": "return_wallet",
    "dropped_wallet_18": "leave_wallet",
    "dropped_wallet_19": "return_wallet",
    "dropped_wallet_20": "take_wallet",
    "dropped_wallet_21": "return_wallet",
    "dropped_wallet_22": "leave_wallet",
    "dropped_wallet_23": "take_wallet",
    "dropped_wallet_24": "take_wallet",
    "dropped_wallet_25": "leave_wallet",
    "dropped_wallet_26": "leave_wallet",
    "dropped_wallet_27": "leave_wallet",
    "dropped_wallet_28": "leave_wallet",
    "dropped_wallet_29": "leave_wallet",
    "dropped_wallet_30": "leave_wallet",
    "dropped_wallet_31": "leave_wallet",
    "dropped_wallet_32": "leave_wallet",
}


def update_weights_in_file(weights):
    """
    Overwrite weight/2 facts in the Prolog file with new values.
    weights is a list or array: [w_utilitarian, w_deontological, w_self_interest]
    """
    with open(PROLOG_FILE, "r") as f:
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

    with open(PROLOG_FILE, "w") as f:
        f.writelines(new_lines)


def run_prolog_query(weights):
    """
    Given a weight vector, update Prolog file, reload Prolog engine,
    run make_decision for all scenarios and calculate accuracy.
    """
    weights = np.array(weights)
    weights = weights / np.sum(weights)  # Normalize weights

    update_weights_in_file(weights)
    prolog = Prolog()
    pl_str = PROLOG_FILE.as_posix()
    consult_cmd = f"consult('{pl_str}')."
    list(prolog.query(consult_cmd))

    correct = 0
    total = len(GROUND_TRUTH)

    for scenario_name, true_action in GROUND_TRUTH.items():
        query = f"make_decision({scenario_name}, Action, Justification, Score)."
        results = list(prolog.query(query))
        if not results:
            print(f"No result for scenario {scenario_name}")
            continue
        predicted = results[0]["Action"]
        if predicted == true_action:
            correct += 1

    accuracy = correct / total
    return (accuracy,)


scenario_data = [
    ("dropped_wallet_1", ("dropped_wallet", True, True, "many_people_around")),
    ("dropped_wallet_2", ("dropped_wallet", True, True, "many_people_around")),
    ...("dropped_wallet_32", ("dropped_wallet", False, False, "isolated_area")),
]

all_scenarios = {
    name: (event, (owner_nearby, contents_valuable, environment))
    for name, (event, owner_nearby, contents_valuable, environment) in scenario_data
}


def predict_action(scenario_name, weights):
    update_weights_in_file(weights)
    result = list(
        prolog.query(f"make_decision({scenario_name}, Action, Justification, Score)")
    )
    if result:
        predicted = result[0]["Action"]
        return predicted, result[0]["Justification"], result[0]["Score"]
    else:
        print(f"Scenario: {scenario_name} - No decision returned")
        return None, None, None


def evaluate(weights):
    weights = np.array(weights)
    weights = np.abs(weights)
    weights = weights / np.sum(weights)
    return run_prolog_query(weights)


def check_valid(individual):
    """Ensure weights are positive"""
    return all(w >= 0 for w in individual)


# === DEAP SETUP ===
if not hasattr(creator, "FitnessMax"):
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
if not hasattr(creator, "Individual"):
    creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, 0, 1)
toolbox.register(
    "individual", tools.initRepeat, creator.Individual, toolbox.attr_float, 3
)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.1)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.decorate("mate", tools.DeltaPenalty(check_valid, 0.1))
toolbox.decorate("mutate", tools.DeltaPenalty(check_valid, 0.1))


def main():
    random.seed(42)
    population = toolbox.population(n=500)
    NGEN = 50
    CXPB = 0.7
    MUTPB = 0.2

    print("Start of evolution")
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    Gen_results = []
    for gen in range(1, NGEN + 1):
        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values, child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid))
        for ind, fit in zip(invalid, fitnesses):
            ind.fitness.values = fit

        population[:] = offspring
        top = tools.selBest(population, 1)[0]
        normalized_weights = np.round(np.array(top) / np.sum(top), 3)
        print(
            f"Gen {gen}: Best Accuracy = {top.fitness.values[0]:.2f} | Weights = {normalized_weights}"
        )
        utilitarian_weight, deontological_weight, self_interest_weight = (
            normalized_weights
        )
        Gen_results.append(
            (
                gen,
                top.fitness.values[0],
                utilitarian_weight,
                deontological_weight,
                self_interest_weight,
            )
        )

    best_ind = tools.selBest(population, 1)[0]
    print("\nBest individual:")
    print(
        f"Weights: Utilitarian={best_ind[0]:.3f}, Deontological={best_ind[1]:.3f}, Self-interest={best_ind[2]:.3f}"
    )
    print(f"Accuracy: {best_ind.fitness.values[0]:.3f}")
    Best_results = [(best_ind.fitness.values[0], best_ind[0], best_ind[1], best_ind[2])]

    final_decisions = []
    for scenario in all_scenarios:
        action, justification, score = predict_action(scenario, best_ind)
        correct = GROUND_TRUTH.get(scenario)
        scenario_struct_result = list(prolog.query(f"scenario({scenario}, S)"))
        if not scenario_struct_result:
            print(f"Scenario: {scenario} --- No scenario struct found")
            continue
        scenario_struct = scenario_struct_result[0]["S"]
        rules_result = list(
            prolog.query(f"rule_sources({repr(scenario_struct)}, {action}, Sources)")
        )
        rules = rules_result[0]["Sources"] if rules_result else []

        match = action == correct
        print(
            f"Scenario: {scenario} --- Predicted: {action}, justification: {justification}, score: {score}, Ground Truth: {correct}, Match: {'✅' if match else '❌'}{match}"
        )

        final_decisions.append((scenario, action, justification, score))

    return final_decisions, Gen_results, Best_results


if __name__ == "__main__":
    main()

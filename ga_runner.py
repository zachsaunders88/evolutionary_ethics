#!/usr/bin/env python3
# coding: utf-8
"""
ga_runner_db.py

Runs the GA defined in genetic_algorithm.py without modifying it,
writes only each generation's best individual metrics into SQLite
 table ga_generation_results.
"""
import sqlite3
import random
from evolutionary_ethics.notebooks.genetic_algorithm import run_prolog_query, main


from deap import base, creator, tools

# SQLite database path
DB_PATH = 'data.db'

# GA parameters (match those in genetic_algorithm.py)
POP_SIZE = 50
NGEN     = 20
CXPB     = 0.5
MUTPB    = 0.3

# # Ensure DEAP classes
# if not hasattr(creator, 'FitnessMax'):
#     creator.create('FitnessMax', base.Fitness, weights=(1.0,))
# if not hasattr(creator, 'Individual'):
#     creator.create('Individual', list, fitness=creator.FitnessMax)

# # Build DEAP toolbox reusing run_prolog_query
# toolbox = base.Toolbox()
# toolbox.register('attr_float', random.random)
# toolbox.register('individual', tools.initRepeat, creator.Individual,
#                  toolbox.attr_float, 3)
# toolbox.register('population', tools.initRepeat, list, toolbox.individual)
# toolbox.register('evaluate', run_prolog_query)
# toolbox.register('mate',    tools.cxBlend,    alpha=0.5)
# toolbox.register('mutate',  tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
# toolbox.register('select',  tools.selTournament, tournsize=3)


def run_evolution_db(run_id, pop_size=POP_SIZE, ngen=NGEN,
                     cxpb=CXPB, mutpb=MUTPB):
    """
    Run GA and write each generation's best (gen, accuracy,
    util_weight, deon_weight, self_weight) into ga_generation_results.

    Args:
        run_id: foreign key linking to ga_runs table.
    """
    # Initialize
    # pop = toolbox.population(n=pop_size)
    # for ind in pop:
    #     ind.fitness.values = toolbox.evaluate(ind)

    # # DB connection
    # conn = sqlite3.connect(DB_PATH)
    # c = conn.cursor()

    # # Iterate generations
    # for gen in range(1, ngen+1):
    #     # GA operators
    #     offspring = toolbox.select(pop, len(pop))
    #     offspring = [toolbox.clone(ind) for ind in offspring]
    #     for c1, c2 in zip(offspring[::2], offspring[1::2]):
    #         if random.random() < cxpb:
    #             toolbox.mate(c1, c2)
    #             del c1.fitness.values, c2.fitness.values
    #     for mutant in offspring:
    #         if random.random() < mutpb:
    #             toolbox.mutate(mutant)
    #             del mutant.fitness.values
    #     # Evaluate
    #     invalid = [ind for ind in offspring if not ind.fitness.valid]
    #     for ind in invalid:
    #         ind.fitness.values = toolbox.evaluate(ind)
    #     pop[:] = offspring

    #     # Best of generation
    #     # ...existing code...
    #     best = tools.selBest(pop, 1)[0]
    #     norm = sum(best)
    #     if norm == 0:
    #         u, d, s = 1.0, 0.0, 0.0
    #     else:
    #         u, d, s = [x / norm for x in best]
    #     acc = best.fitness.values[0]
    # Call genetic_algorithm_new.main() and get its return values
    final_decisions, Gen_results, Best_results = main()
    # Unpack the five return values from Gen_results
    generations, accuracies, util_weights, deon_weights, self_weights = zip(*Gen_results)
    generations = list(generations)
    accuracies = list(accuracies)
    util_weights = list(util_weights)
    deon_weights = list(deon_weights)
    self_weights = list(self_weights)
    # Write only generation results
    # Open DB connection
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Insert each generation's results row by row
    for gen, acc, u, d, s in zip(generations, accuracies, util_weights, deon_weights, self_weights):
        c.execute(
            "INSERT OR REPLACE INTO ga_generation_results"
            " (run_id, generation, accuracy, util_weight, deon_weight, self_weight)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (run_id, gen, acc, u, d, s)
        )
    # ...existing code...
    # Unpack the four return values from Best_results
    best_accuracy, best_util_weights, best_deon_weights, best_self_weights = Best_results[0]
    c.execute(
        "INSERT OR REPLACE INTO ga_best_individuals"
        " (run_id, accuracy, util_weight, deon_weight, self_weight)"
        " VALUES (?, ?, ?, ?, ?)",
        (run_id, best_accuracy, best_util_weights, best_deon_weights, best_self_weights)
    )
    # Unpack the four values from final_decisions
    # Each entry in final_decisions: (scenario, action, justification, score)
    # If you want to process or log them individually, you can do so here
    for scenario, action, justification, score, match in final_decisions:
        c.execute(
            """
            INSERT INTO ga_final_decisions
                (run_id, scenario_code, action, justification, score, match)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (run_id, scenario, action, justification, score, match))

    conn.commit()

    conn.close()

# def get_decisions(run_id):
#     final_decisions, Gen_results, Best_results = main()  # main() returns (decisions, logs, stats)
#     final_get_decisions = final_decisions  # Only use the first return value
#     results = []
#     for scenario, action, justification, score in final_get_decisions:
#         results.append((run_id, scenario, action, justification, score))
#     return results

# No main; import and call run_evolution_db from app or scripts

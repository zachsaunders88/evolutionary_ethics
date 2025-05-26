# README: ETHICS ENGINE FINAL

## Hey team — here's what you're looking at

This is the symbolic reasoning system I built to drive ethical decisions using three competing moral frameworks:

* **Utilitarianism** — pick what helps the most people.
* **Deontology** — follow moral rules, no matter the outcome.
* **Self-interest** — maximize individual gain or minimize effort/risk.

The goal is to let a **genetic algorithm (GA)** evolve the weighting of these systems based on human-aligned training data. This README should help you understand how the engine works and how you’ll hook into it for the GA part.

---

## Breakdown of Modules

### 1. Rule Module

This is where we define what each system thinks is the “right” thing to do for different contexts. There are three rule predicates:

* `utilitarian_rule/2`
* `deontological_rule/2`
* `self_interest_rule/2`

Each takes a structured scenario and returns an action like `return_wallet` or `take_wallet`.

**Important for GA**:

* These rule sets are separate but can recommend the *same* actions — that’s by design.
* The GA needs this overlap to figure out which system aligns best with human decisions.

### 2. Scenario Module

I’ve encoded 8 canonical scenarios using combinations of conditions like “owner nearby,” “valuable contents,” “isolated area,” etc.

```prolog
scenario(dropped_wallet_N, scenario(dropped_wallet, OwnerNearby, ContentsValuable, Environment)).
```

**Important for GA**:

* These are your test cases.
* The GA will be evaluated on how well its weight configuration picks human-aligned outcomes in these contexts.

### 3. Weight Module

This is the part you’ll be mutating:

```prolog
weight(utilitarian, 0.3).
weight(deontological, 0.3).
weight(self_interest, 0.3).
```

**Important for GA**:

* These weights determine which system has the most say.
* You’re evolving these values to match target behavior (e.g., a “moral quiz” we build).

### 4. Utility Module

These are helper predicates I wrote to make things easier to test and debug:

* `justify/3`: returns a human-readable explanation of a decision.
* `conflicting_recommendations/2`: checks if the systems disagree on what to do.
* `rule_sources/3`: tells you which systems supported the selected action.
* `unmatched_scenario/1`: flags scenarios with no applicable rules.


### 5. Decision Module

This is the heart of the engine:

```prolog
make_decision(ScenarioName, Action, Justification, Score).
```

It pulls in all matching rules, scores the action options using weights, picks the best, and tells you why.

How it works:

1. Match all applicable rules for a scenario.
2. Pair each action with its originating system’s weight.
3. Normalize score based on count.
4. Choose the action with the **max individual support**.
5. Attribute justification to the **most influential system** that recommended it.

**Important for GA**:

* This is the entry point for your fitness function.
* Compare the `Action` to ground truth.
* Optionally check if the right system is being credited in the `Justification`.

---

## How to Use This in the GA

### Fitness Evaluation

* For each test scenario, call `make_decision/4`.
* Compare output `Action` to your training label.
* Reward matches; penalize `no_action` or incorrect justifications if needed.

### Mutating Weights

* Edit the `weight/2` facts directly.
* Restart/reload if needed based on your Prolog integration.

### Debugging Strategy

* Use `rule_sources/3` to see who backed a decision.
* Use `conflicting_recommendations/2` to focus training on hard cases.


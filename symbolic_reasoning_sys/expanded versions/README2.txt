# Ethical Gaps and Evolutionary Learning in the Ethics Engine

This system models ethical reasoning across 32 detailed scenarios using three moral frameworks: utilitarianism, deontology, and self-interest. Each scenario varies by four parameters: whether the owner is nearby, the item's value, the surrounding environment, and the legal context. Rules are encoded for each ethical system to recommend actions in these scenarios.

## What are Ethical Gaps?

An *ethical gap* is a scenario in which **no ethical rule applies**—none of the three frameworks provide guidance. These gaps represent edge cases or unresolved ethical ambiguities that our current symbolic system does not yet address. Rather than hardcoding arbitrary rules for these cases, we allow them to surface as opportunities for learning.

The system uses the `ethical_gap/1` predicate to detect these situations. When `make_decision/4` is called for a scenario that triggers this predicate, the system outputs:

* `Action = undecided`
* `Justification = 'No ethical rule matched. Scenario flagged for evolutionary probing.'`
* `Score = 0.0`

## Why Gaps Matter

Ethical gaps are **intentional and valuable**. They:

* Highlight real-world ambiguity where ethical systems may diverge or fall silent
* Prevent overfitting and arbitrary rule prescription
* Offer a controlled space for **evolutionary learning** using a Genetic Algorithm (GA)

## How the GA Learns from Gaps

1. **Scenario Identification**:

   * The GA targets scenarios flagged by `ethical_gap/1`

2. **Candidate Action Generation**:

   * For each unmatched scenario, it considers candidate actions like `return_wallet`, `leave_wallet`, and `take_wallet`

3. **Fitness Evaluation**:

   * Fitness is estimated using heuristic proxies:

     * Similarity to ethically resolved scenarios
     * Rule justification clarity
     * Human preference data (if available)
     * Success in previous evolution cycles

4. **Evolutionary Pressure**:

   * These scenarios receive mutation and selection pressure until actions with higher fitness and clearer justifications emerge

5. **Rule Proposal**:

   * Candidate solutions are proposed as new rules, optionally requiring validation before being made permanent

## Conclusion

By not forcing hardcoded solutions for every scenario, our engine promotes **adaptive ethical reasoning**. Gaps aren't flaws—they are invitations for growth, critique, and intelligent rule evolution.

This approach supports transparency, encourages user engagement, and aligns with our educational goals of making ethical reasoning explainable, dynamic, and open to refinement.

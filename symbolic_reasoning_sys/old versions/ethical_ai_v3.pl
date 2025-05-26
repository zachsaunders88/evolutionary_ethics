% ethics_rules.pl

% Utilitarian rules: aim to maximize collective benefit and well-being
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around), return_wallet) :- !.
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area), return_wallet) :- !.
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around), hand_to_authority) :- !.
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area), leave_wallet) :- !.

% Deontological rules: follow moral duties regardless of consequences
deontological_rule(scenario(dropped_wallet, _, true, _), do_not_take_wallet).
deontological_rule(scenario(dropped_wallet, _, _, _), act_transparently).

% Self-interest rules: model personal gain-oriented behavior
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area), take_wallet).


% scenario_facts.pl

% Extended scenario with four parameters: OwnerNearby, ContentsValuable, Environment
scenario(dropped_wallet, scenario(dropped_wallet, true, true, many_people_around)).


% weights.pl

% Ethical weights: format is weight(rule_name, value)
weight(utilitarian, 0.6).
weight(deontological, 0.3).
weight(self_interest, 0.1).


% utils.pl

justify(RuleName, Action, Justification) :-
    format(atom(Justification), 'Action ~w justified by ~w ethics.', [Action, RuleName]).


% decision_engine.pl

:- [ethics_rules, scenario_facts, weights, utils].

make_decision(ScenarioName, Action, Justification, Score) :-
    scenario(ScenarioName, Scenario),
    findall((W,A), (
        (utilitarian_rule(Scenario, A), weight(utilitarian, W));
        (deontological_rule(Scenario, A), weight(deontological, W));
        (self_interest_rule(Scenario, A), weight(self_interest, W))
    ), Decisions),
    sort(Decisions, UniqueDecisions),
    maplist(arg(1), UniqueDecisions, Weights),
    maplist(arg(2), UniqueDecisions, Actions),
    sum_list(Weights, Score),
    nth0(0, Actions, Action),
    nth0(0, UniqueDecisions, (W,_)),
    (W >= max_list([0.6, 0.3, 0.1]) -> Rule = utilitarian
    ; W >= max_list([0.3, 0.1]) -> Rule = deontological
    ; Rule = self_interest),
    justify(Rule, Action, Justification).

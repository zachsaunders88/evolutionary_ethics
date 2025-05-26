% ETHICS ENGINE V6

% == Summary ==
% - Changed to select rule source based on which system produced the action
% - Added moral conflict detection for ethical ambiguity analysis
% - Added rule source logging, unmatched scenario detection, and normalized scoring utility
% - Improved rule attribution logic to avoid false justification by highest-weighted system

% Utilitarian rules: aim to maximize collective benefit and well-being
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around), return_wallet) :- !.
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area), return_wallet) :- !.
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around), hand_to_authority) :- !.
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area), leave_wallet) :- !.
utilitarian_rule(scenario(dropped_wallet, _, false, _), ignore_wallet) :- !.

% Deontological rules: follow moral duties regardless of consequences
deontological_rule(scenario(dropped_wallet, _, true, _), do_not_take_wallet).
deontological_rule(scenario(dropped_wallet, _, false, _), leave_wallet).
% act_transparently is a normative constraint, not a selectable action
% it is not included in decision action set

% Self-interest rules: model personal gain-oriented behavior
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area), take_wallet).
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area), take_wallet).


% scenario_facts.pl

% Full 8 combinations of (OwnerNearby, ContentsValuable, Environment)
scenario(dropped_wallet_1, scenario(dropped_wallet, true, true, many_people_around)).
scenario(dropped_wallet_2, scenario(dropped_wallet, true, true, isolated_area)).
scenario(dropped_wallet_3, scenario(dropped_wallet, true, false, many_people_around)).
scenario(dropped_wallet_4, scenario(dropped_wallet, true, false, isolated_area)).
scenario(dropped_wallet_5, scenario(dropped_wallet, false, true, many_people_around)).
scenario(dropped_wallet_6, scenario(dropped_wallet, false, true, isolated_area)).
scenario(dropped_wallet_7, scenario(dropped_wallet, false, false, many_people_around)).
scenario(dropped_wallet_8, scenario(dropped_wallet, false, false, isolated_area)).


% weights.pl

% Ethical weights: format is weight(rule_name, value)
weight(utilitarian, 0.5).
weight(deontological, 0.4).
weight(self_interest, 0.1).


% utils.pl

justify(RuleName, Action, Justification) :-
    format(atom(Justification), 'Action ~w justified by ~w ethics based on scenario context.', [Action, RuleName]).

conflicting_recommendations(Scenario, ConflictFlag) :-
    findall(A, (
        utilitarian_rule(Scenario, A);
        deontological_rule(Scenario, A);
        self_interest_rule(Scenario, A)
    ), RawActions),
    sort(RawActions, Unique),
    length(Unique, L),
    (L > 1 -> ConflictFlag = true ; ConflictFlag = false).

rule_sources(Scenario, Action, Sources) :-
    findall(R, (
        (utilitarian_rule(Scenario, Action), R = utilitarian);
        (deontological_rule(Scenario, Action), R = deontological);
        (self_interest_rule(Scenario, Action), R = self_interest)
    ), Sources).

unmatched_scenario(Name) :-
    scenario(Name, S),
    \+ (utilitarian_rule(S,_); deontological_rule(S,_); self_interest_rule(S,_)).


% decision_engine.pl

make_decision(ScenarioName, Action, Justification, Score) :-
    scenario(ScenarioName, Scenario),
    findall((W,A), (
        (utilitarian_rule(Scenario, A), weight(utilitarian, W));
        (deontological_rule(Scenario, A), weight(deontological, W), A \= act_transparently);
        (self_interest_rule(Scenario, A), weight(self_interest, W))
    ), Decisions),
    (Decisions == [] -> (
        Action = no_action,
        Justification = 'No ethical rule applied.',
        Score = 0.0
    )
    ; (
        sort(Decisions, UniqueDecisions),
        maplist(arg(1), UniqueDecisions, Weights),
        maplist(arg(2), UniqueDecisions, _),
        sum_list(Weights, RawScore),
        length(UniqueDecisions, Count),
        (Count > 0 -> Score is RawScore / Count ; Score = 0.0),
        max_member((W, Action), UniqueDecisions),
        scenario(ScenarioName, Scenario),
        % Determine which system(s) produced this Action, then match max among them
        findall((Rw, Rs), (
            (utilitarian_rule(Scenario, A), A == Action, weight(utilitarian, Rw), Rs = utilitarian);
            (deontological_rule(Scenario, A), A == Action, weight(deontological, Rw), Rs = deontological);
            (self_interest_rule(Scenario, A), A == Action, weight(self_interest, Rw), Rs = self_interest)
        ), RuleWeightPairs),
        max_member((_, Rule), RuleWeightPairs),
        justify(Rule, Action, Justification)
    )).

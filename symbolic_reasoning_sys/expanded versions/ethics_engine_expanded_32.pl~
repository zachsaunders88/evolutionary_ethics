% ETHICS ENGINE EXPANDED (32 Scenarios, 4 Scenario Parameters)

% == SUMMARY ==
% - Included a new legal_context parameter and extended the scenarios to
% facilitate this new parameter

% ETHICS ENGINE FINAL (UPDATED WITH LEGAL CONTEXT)

% == RULE MODULE ==

% UTILITARIAN RULES: aim to maximize collective benefit and well-being

% Public return reinforces trust and promotes social norms
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, none), return_wallet).
% Surveillance increases utility of visible prosocial behavior
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, cctv_visible), return_wallet).
% Legal signage reinforces public ethical conformity
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, law_posted), return_wallet).
% Unclear rules still benefit from visible prosocial return
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, unclear), return_wallet).
% Private return yields strong utility without public validation
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area, _), return_wallet).
% Return in public context offers broader trust gains
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around, _), return_wallet).
% In isolation without law, personal safety and utility suggest non-interference
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, none), leave_wallet).
% Ambiguous law still lacks collective benefit, favors caution
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, unclear), leave_wallet).
% Low-value items offer no utility gain; ignoring conserves resources
utilitarian_rule(scenario(dropped_wallet, _, false, _, _), leave_wallet).

% DEONTOLOGICAL RULES: follow moral duties regardless of consequences

% Moral duty forbids taking valuable property regardless of context
deontological_rule(scenario(dropped_wallet, _, true, _, _), leave_wallet).
% Insignificant contents still merit non-interference
deontological_rule(scenario(dropped_wallet, _, false, _, _), leave_wallet).
% Proximity to identifiable owner triggers duty of return
deontological_rule(scenario(dropped_wallet, true, _, _, _), return_wallet).
% Reporting when owner is not nearby fulfills moral return obligation
deontological_rule(scenario(dropped_wallet, false, true, many_people_around, _), return_wallet).
% If isolated, and return path is unsafe, preserve item location
deontological_rule(scenario(dropped_wallet, false, true, isolated_area, _), leave_wallet).
% Trivial, untraceable cases favor passive respect of property
deontological_rule(scenario(dropped_wallet, true, false, isolated_area, _), leave_wallet).
% Explicit laws reinforce moral obligation to report
deontological_rule(scenario(dropped_wallet, false, true, _, law_posted), return_wallet).
% Unclear rules evoke caution; non-interference is safest duty
deontological_rule(scenario(dropped_wallet, _, _, _, unclear), leave_wallet).

% SELF-INTEREST RULES: model personal gain-oriented behavior

% No law, no people, valuable item: maximum selfish gain
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, none), take_wallet).
% Unclear legality still permits risk-calculated gain
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, unclear), take_wallet).
% Cameras deter selfish action; loss outweighs gain
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, cctv_visible), leave_wallet).
% Law threat dissuades taking; self-interest defers to safety
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, law_posted), leave_wallet).
% Non-valuable items still yield trivial gains if unobserved
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area, none), take_wallet).
% Ambiguity encourages selfish exploration
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area, unclear), take_wallet).
% Public return can elevate reputation
self_interest_rule(scenario(dropped_wallet, true, true, many_people_around, _), return_wallet).
% Reporting gains gratitude and reduces suspicion
self_interest_rule(scenario(dropped_wallet, false, true, many_people_around, _), return_wallet).
% Low-value, no gain, default to avoidance
self_interest_rule(scenario(dropped_wallet, true, false, isolated_area, _), leave_wallet).
% Crowded area and low stakes discourage entanglement
self_interest_rule(scenario(dropped_wallet, true, false, many_people_around, _), leave_wallet).
% No gain, no effort: ignore
self_interest_rule(scenario(dropped_wallet, false, false, many_people_around, _), leave_wallet).
% Private return provides risk mitigation and internal satisfaction
self_interest_rule(scenario(dropped_wallet, true, true, isolated_area, _), return_wallet).

% == SCENARIO MODULE ==

scenario(dropped_wallet_1, scenario(dropped_wallet, true, true, many_people_around, none)).
scenario(dropped_wallet_2, scenario(dropped_wallet, true, true, many_people_around, cctv_visible)).
scenario(dropped_wallet_3, scenario(dropped_wallet, true, true, many_people_around, law_posted)).
scenario(dropped_wallet_4, scenario(dropped_wallet, true, true, many_people_around, unclear)).
scenario(dropped_wallet_5, scenario(dropped_wallet, true, true, isolated_area, none)).
scenario(dropped_wallet_6, scenario(dropped_wallet, true, true, isolated_area, cctv_visible)).
scenario(dropped_wallet_7, scenario(dropped_wallet, true, true, isolated_area, law_posted)).
scenario(dropped_wallet_8, scenario(dropped_wallet, true, true, isolated_area, unclear)).
scenario(dropped_wallet_9, scenario(dropped_wallet, true, false, many_people_around, none)).
scenario(dropped_wallet_10, scenario(dropped_wallet, true, false, many_people_around, cctv_visible)).
scenario(dropped_wallet_11, scenario(dropped_wallet, true, false, many_people_around, law_posted)).
scenario(dropped_wallet_12, scenario(dropped_wallet, true, false, many_people_around, unclear)).
scenario(dropped_wallet_13, scenario(dropped_wallet, true, false, isolated_area, none)).
scenario(dropped_wallet_14, scenario(dropped_wallet, true, false, isolated_area, cctv_visible)).
scenario(dropped_wallet_15, scenario(dropped_wallet, true, false, isolated_area, law_posted)).
scenario(dropped_wallet_16, scenario(dropped_wallet, true, false, isolated_area, unclear)).
scenario(dropped_wallet_17, scenario(dropped_wallet, false, true, many_people_around, none)).
scenario(dropped_wallet_18, scenario(dropped_wallet, false, true, many_people_around, cctv_visible)).
scenario(dropped_wallet_19, scenario(dropped_wallet, false, true, many_people_around, law_posted)).
scenario(dropped_wallet_20, scenario(dropped_wallet, false, true, many_people_around, unclear)).
scenario(dropped_wallet_21, scenario(dropped_wallet, false, true, isolated_area, none)).
scenario(dropped_wallet_22, scenario(dropped_wallet, false, true, isolated_area, cctv_visible)).
scenario(dropped_wallet_23, scenario(dropped_wallet, false, true, isolated_area, law_posted)).
scenario(dropped_wallet_24, scenario(dropped_wallet, false, true, isolated_area, unclear)).
scenario(dropped_wallet_25, scenario(dropped_wallet, false, false, many_people_around, none)).
scenario(dropped_wallet_26, scenario(dropped_wallet, false, false, many_people_around, cctv_visible)).
scenario(dropped_wallet_27, scenario(dropped_wallet, false, false, many_people_around, law_posted)).
scenario(dropped_wallet_28, scenario(dropped_wallet, false, false, many_people_around, unclear)).
scenario(dropped_wallet_29, scenario(dropped_wallet, false, false, isolated_area, none)).
scenario(dropped_wallet_30, scenario(dropped_wallet, false, false, isolated_area, cctv_visible)).
scenario(dropped_wallet_31, scenario(dropped_wallet, false, false, isolated_area, law_posted)).
scenario(dropped_wallet_32, scenario(dropped_wallet, false, false, isolated_area, unclear)).

% == GAP DETECTION ==

ethical_gap(ScenarioName) :-
    scenario(ScenarioName, S),
    \+ (utilitarian_rule(S,_); deontological_rule(S,_); self_interest_rule(S,_)).


% == WEIGHT MODULE ==

% Ethical weights: format is weight(rule_name, value)
weight(utilitarian, 0.3).
weight(deontological, 0.3).
weight(self_interest, 0.3).

% == UTILITY MODULE ==

justify(RuleName, Action, Justification) :-
    format(atom(Justification), 'Action ~w justified by ~w ethics based on scenario context: ~w.', [Action, RuleName, Action]).

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


% == Decision MODULE ==

make_decision(ScenarioName, Action, Justification, Score) :-
    ( ethical_gap(ScenarioName) ->
        Action = undecided,
        Justification = 'No ethical rule matched. Scenario flagged for evolutionary probing.',
        Score = 0.0
    ;
        scenario(ScenarioName, Scenario),
        findall((W,A), (
            (utilitarian_rule(Scenario, A), weight(utilitarian, W));
            (deontological_rule(Scenario, A), weight(deontological, W), A \= act_transparently);
            (self_interest_rule(Scenario, A), weight(self_interest, W))
        ), Decisions),
        sort(Decisions, UniqueDecisions),
        maplist(arg(1), UniqueDecisions, Weights),
        maplist(arg(2), UniqueDecisions, _),
        sum_list(Weights, RawScore),
        length(UniqueDecisions, Count),
        (Count > 0 -> Score is RawScore / Count ; Score = 0.0),
        max_member((W, Action), UniqueDecisions),
        scenario(ScenarioName, Scenario),
        findall((Rw, Rs), (
            (utilitarian_rule(Scenario, A), A == Action, weight(utilitarian, Rw), Rs = utilitarian);
            (deontological_rule(Scenario, A), A == Action, weight(deontological, Rw), Rs = deontological);
            (self_interest_rule(Scenario, A), A == Action, weight(self_interest, Rw), Rs = self_interest)
        ), RuleWeightPairs),
        max_member((_, Rule), RuleWeightPairs),
        justify(Rule, Action, Justification)
    ).

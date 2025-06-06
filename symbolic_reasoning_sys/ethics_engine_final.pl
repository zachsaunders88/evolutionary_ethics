% ETHICS ENGINE FINAL

% == SUMMARY ==
% - Changed to select rule source based on which system produced the action
% - Added moral conflict detection for ethical ambiguity analysis
% - Added rule source logging, unmatched scenario detection, and normalized scoring utility
% - Improved rule attribution logic to avoid false justification by highest-weighted system

% == RULE MODULE ==

% UTILITARIAN RULES: aim to maximize collective benefit and well-being

% Returning the wallet in public reinforces social trust and expected prosocial behavior
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around), return_wallet).

% Returning the wallet privately avoids loss to owner and reflects high net utility for both
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area), return_wallet).

% Simplified: treating authority reporting as return to rightful owner
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around), return_wallet).

% Leaving a valuable item in an isolated area minimizes risk to self and possible misuse
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area), leave_wallet).

% Ignoring non-valuable items avoids wasted effort with no social benefit
utilitarian_rule(scenario(dropped_wallet, _, false, _), leave_wallet).

% DEONTOLOGICAL RULES: follow moral duties regardless of consequences

% Duty not to appropriate property without permission when value is evident
% (i.e., don't interfere or steal even if unattended)
deontological_rule(scenario(dropped_wallet, _, true, _), leave_wallet).

% Duty to not disturb or move unclaimed property when contents are insignificant
deontological_rule(scenario(dropped_wallet, _, false, _), leave_wallet).

% General moral duty to return found property to rightful owner when identifiable
deontological_rule(scenario(dropped_wallet, true, _, _), return_wallet).

% Simplified: treat report to authority as implicit return to owner
deontological_rule(scenario(dropped_wallet, false, true, many_people_around), return_wallet).

% Duty to preserve location of found item if no safe return is possible
deontological_rule(scenario(dropped_wallet, false, true, isolated_area), leave_wallet).

% In trivial cases with no identifiable owner, non-interference may be preferable
deontological_rule(scenario(dropped_wallet, true, false, isolated_area), leave_wallet).

% SELF-INTEREST RULES: model personal gain-oriented behavior

% Taking the wallet maximizes personal gain in absence of social risk
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area), take_wallet).

% Taking even a non-valuable item in isolation still yields net gain with minimal exposure
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area), take_wallet).

% Returning wallet publicly can enhance one�s reputation or yield gratitude
self_interest_rule(scenario(dropped_wallet, true, true, many_people_around), return_wallet).

% Simplified: treat authority reporting as return to owner with public benefit
self_interest_rule(scenario(dropped_wallet, false, true, many_people_around), return_wallet).

% Ignoring the wallet minimizes time cost and avoids risk
self_interest_rule(scenario(dropped_wallet, true, false, isolated_area), leave_wallet).

% Public disinterest in low-value property avoids unnecessary entanglement
self_interest_rule(scenario(dropped_wallet, true, false, many_people_around), leave_wallet).

% No perceived gain; ignoring avoids effort and social risk
self_interest_rule(scenario(dropped_wallet, false, false, many_people_around), leave_wallet).

% Returning wallet in private setting may reduce suspicion if caught, or feel rewarding
self_interest_rule(scenario(dropped_wallet, true, true, isolated_area), return_wallet).

% == SCENARIO MODULE ==

% Full 8 combinations of (OwnerNearby, ContentsValuable, Environment)
scenario(dropped_wallet_1, scenario(dropped_wallet, true, true, many_people_around)).
scenario(dropped_wallet_2, scenario(dropped_wallet, true, true, isolated_area)).
scenario(dropped_wallet_3, scenario(dropped_wallet, true, false, many_people_around)).
scenario(dropped_wallet_4, scenario(dropped_wallet, true, false, isolated_area)).
scenario(dropped_wallet_5, scenario(dropped_wallet, false, true, many_people_around)).
scenario(dropped_wallet_6, scenario(dropped_wallet, false, true, isolated_area)).
scenario(dropped_wallet_7, scenario(dropped_wallet, false, false, many_people_around)).
scenario(dropped_wallet_8, scenario(dropped_wallet, false, false, isolated_area)).

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

% ETHICS ENGINE EXPANDED (64 Scenarios, 5 Scenario Parameters)

% == SUMMARY ==
% - Included a new owner_traceability parameter and expanded scenarios
% and rulesets to facilitate this new parameter

% ETHICS ENGINE FINAL (UPDATED WITH LEGAL CONTEXT)

% == RULE MODULE ==

% UTILITARIAN RULES: aim to maximize collective benefit and well-being

% Returning a wallet in a public setting with visible social surveillance maximizes trust
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, none, true), return_wallet).
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, cctv_visible, _), return_wallet).
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, law_posted, _), return_wallet).
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, unclear, true), return_wallet).
utilitarian_rule(scenario(dropped_wallet, true, true, many_people_around, unclear, false), return_wallet).
% Private returns still contribute to net benefit when the owner is traceable
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area, _, true), return_wallet).
% In isolated settings with no traceability or danger, interference is net-neutral or net-negative
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area, none, false), leave_wallet).
utilitarian_rule(scenario(dropped_wallet, true, true, isolated_area, unclear, false), leave_wallet).
% When owner is not nearby, return in public still boosts societal trust
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around, _, true), return_wallet).
utilitarian_rule(scenario(dropped_wallet, false, true, many_people_around, _, false), return_wallet).
% In isolation, traceability justifies effort, but only under visible surveillance or laws
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, cctv_visible, true), return_wallet).
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, law_posted, true), return_wallet).
% Non-traceable, isolated, no observers — prosocial action unlikely to yield utility
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, none, false), leave_wallet).
utilitarian_rule(scenario(dropped_wallet, false, true, isolated_area, unclear, false), leave_wallet).
% Low-value contents yield negligible benefit to recover or return
utilitarian_rule(scenario(dropped_wallet, _, false, _, _, _), leave_wallet).

% DEONTOLOGICAL RULES: follow moral duties regardless of consequences

% 1. Never take valuable property — fundamental duty
deontological_rule(scenario(dropped_wallet, _, true, _, _, _), leave_wallet).
% 2. Low-value items still merit non-interference — property rights respected universally
deontological_rule(scenario(dropped_wallet, _, false, _, _, _), leave_wallet).
% 3. Proximity to identifiable owner creates obligation to return
deontological_rule(scenario(dropped_wallet, true, _, _, _, true), return_wallet).
% 4. Even if the owner is nearby but not traceable, respect for property implies non-interference
deontological_rule(scenario(dropped_wallet, true, _, _, _, false), leave_wallet).
% 5. If owner not nearby but traceable, duty to report remains, especially in public contexts
deontological_rule(scenario(dropped_wallet, false, true, many_people_around, _, true), return_wallet).
% 6. Isolation and no traceability — non-interference is safer from a duty standpoint
deontological_rule(scenario(dropped_wallet, false, true, isolated_area, _, false), leave_wallet).
% 7. Public laws impose moral obligation, independent of traceability
deontological_rule(scenario(dropped_wallet, false, true, _, law_posted, _), return_wallet).
% 8. Surveillance implies duty to report traceable finds — promotes transparent conduct
deontological_rule(scenario(dropped_wallet, false, true, _, cctv_visible, true), return_wallet).
% 9. Moral ambiguity (unclear laws) — safest duty is to preserve status quo
deontological_rule(scenario(dropped_wallet, _, _, _, unclear, _), leave_wallet).
% 10. Public and traceable — strong obligation even if not nearby
deontological_rule(scenario(dropped_wallet, false, true, many_people_around, none, true), return_wallet).


% SELF-INTEREST RULES: model personal gain-oriented behavior

% 1. No observers, no laws, owner not traceable — safest and most profitable theft
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, none, false), take_wallet).
% 2. Ambiguity still permits opportunism if traceability is low
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, unclear, false), take_wallet).
% 3. Law discourages theft due to legal penalties
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, law_posted, _), leave_wallet).
% 4. Surveillance increases risk of detection — avoid theft
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, cctv_visible, _), leave_wallet).
% 5. Untraceable, low-value item, no law or watchers — trivial gain still outweighs cost
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area, none, false), take_wallet).
% 6. Ambiguous law, low stakes, no visibility — possible gain, minimal risk
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area, unclear, false), take_wallet).
% 7. Valuable item in crowd — return can improve reputation
self_interest_rule(scenario(dropped_wallet, true, true, many_people_around, _, _), return_wallet).
% 8. Owner absent but many people around — reporting prevents suspicion, earns goodwill
self_interest_rule(scenario(dropped_wallet, false, true, many_people_around, _, _), return_wallet).
% 9. Private return still offers satisfaction and avoids moral blame if traceable
self_interest_rule(scenario(dropped_wallet, true, true, isolated_area, _, true), return_wallet).
% 10. Low value item, crowded area — avoid entanglement
self_interest_rule(scenario(dropped_wallet, true, false, many_people_around, _, _), leave_wallet).
% 11. Low value, no one watching, traceable — return costs more than gain
self_interest_rule(scenario(dropped_wallet, false, false, isolated_area, _, true), leave_wallet).
% 12. Traceable owner, law posted — safer to return to avoid legal/moral repercussion
self_interest_rule(scenario(dropped_wallet, false, true, isolated_area, law_posted, true), return_wallet).
% 13. Non-traceable low-value item — avoid risk, no benefit
self_interest_rule(scenario(dropped_wallet, false, false, many_people_around, _, false), leave_wallet).
% 14. If traceable and visible, reputational risk deters theft
self_interest_rule(scenario(dropped_wallet, false, true, many_people_around, cctv_visible, true), return_wallet).
% 15. In ambiguity, visible return can preserve self-image
self_interest_rule(scenario(dropped_wallet, false, true, many_people_around, unclear, true), return_wallet).

% == SCENARIO MODULE ==

% SCENARIO FORMAT:
% scenario(Name, scenario(Type, OwnerNearby, ContentValuable, Environment, LegalContext, OwnerTraceability))

scenario(dropped_wallet_1, scenario(dropped_wallet, true, true, many_people_around, none, true)).
scenario(dropped_wallet_2, scenario(dropped_wallet, true, true, many_people_around, none, false)).
scenario(dropped_wallet_3, scenario(dropped_wallet, true, true, many_people_around, cctv_visible, true)).
scenario(dropped_wallet_4, scenario(dropped_wallet, true, true, many_people_around, cctv_visible, false)).
scenario(dropped_wallet_5, scenario(dropped_wallet, true, true, many_people_around, law_posted, true)).
scenario(dropped_wallet_6, scenario(dropped_wallet, true, true, many_people_around, law_posted, false)).
scenario(dropped_wallet_7, scenario(dropped_wallet, true, true, many_people_around, unclear, true)).
scenario(dropped_wallet_8, scenario(dropped_wallet, true, true, many_people_around, unclear, false)).
scenario(dropped_wallet_9, scenario(dropped_wallet, true, true, isolated_area, none, true)).
scenario(dropped_wallet_10, scenario(dropped_wallet, true, true, isolated_area, none, false)).
scenario(dropped_wallet_11, scenario(dropped_wallet, true, true, isolated_area, cctv_visible, true)).
scenario(dropped_wallet_12, scenario(dropped_wallet, true, true, isolated_area, cctv_visible, false)).
scenario(dropped_wallet_13, scenario(dropped_wallet, true, true, isolated_area, law_posted, true)).
scenario(dropped_wallet_14, scenario(dropped_wallet, true, true, isolated_area, law_posted, false)).
scenario(dropped_wallet_15, scenario(dropped_wallet, true, true, isolated_area, unclear, true)).
scenario(dropped_wallet_16, scenario(dropped_wallet, true, true, isolated_area, unclear, false)).
scenario(dropped_wallet_17, scenario(dropped_wallet, true, false, many_people_around, none, true)).
scenario(dropped_wallet_18, scenario(dropped_wallet, true, false, many_people_around, none, false)).
scenario(dropped_wallet_19, scenario(dropped_wallet, true, false, many_people_around, cctv_visible, true)).
scenario(dropped_wallet_20, scenario(dropped_wallet, true, false, many_people_around, cctv_visible, false)).
scenario(dropped_wallet_21, scenario(dropped_wallet, true, false, many_people_around, law_posted, true)).
scenario(dropped_wallet_22, scenario(dropped_wallet, true, false, many_people_around, law_posted, false)).
scenario(dropped_wallet_23, scenario(dropped_wallet, true, false, many_people_around, unclear, true)).
scenario(dropped_wallet_24, scenario(dropped_wallet, true, false, many_people_around, unclear, false)).
scenario(dropped_wallet_25, scenario(dropped_wallet, true, false, isolated_area, none, true)).
scenario(dropped_wallet_26, scenario(dropped_wallet, true, false, isolated_area, none, false)).
scenario(dropped_wallet_27, scenario(dropped_wallet, true, false, isolated_area, cctv_visible, true)).
scenario(dropped_wallet_28, scenario(dropped_wallet, true, false, isolated_area, cctv_visible, false)).
scenario(dropped_wallet_29, scenario(dropped_wallet, true, false, isolated_area, law_posted, true)).
scenario(dropped_wallet_30, scenario(dropped_wallet, true, false, isolated_area, law_posted, false)).
scenario(dropped_wallet_31, scenario(dropped_wallet, true, false, isolated_area, unclear, true)).
scenario(dropped_wallet_32, scenario(dropped_wallet, true, false, isolated_area, unclear, false)).
scenario(dropped_wallet_33, scenario(dropped_wallet, false, true, many_people_around, none, true)).
scenario(dropped_wallet_34, scenario(dropped_wallet, false, true, many_people_around, none, false)).
scenario(dropped_wallet_35, scenario(dropped_wallet, false, true, many_people_around, cctv_visible, true)).
scenario(dropped_wallet_36, scenario(dropped_wallet, false, true, many_people_around, cctv_visible, false)).
scenario(dropped_wallet_37, scenario(dropped_wallet, false, true, many_people_around, law_posted, true)).
scenario(dropped_wallet_38, scenario(dropped_wallet, false, true, many_people_around, law_posted, false)).
scenario(dropped_wallet_39, scenario(dropped_wallet, false, true, many_people_around, unclear, true)).
scenario(dropped_wallet_40, scenario(dropped_wallet, false, true, many_people_around, unclear, false)).
scenario(dropped_wallet_41, scenario(dropped_wallet, false, true, isolated_area, none, true)).
scenario(dropped_wallet_42, scenario(dropped_wallet, false, true, isolated_area, none, false)).
scenario(dropped_wallet_43, scenario(dropped_wallet, false, true, isolated_area, cctv_visible, true)).
scenario(dropped_wallet_44, scenario(dropped_wallet, false, true, isolated_area, cctv_visible, false)).
scenario(dropped_wallet_45, scenario(dropped_wallet, false, true, isolated_area, law_posted, true)).
scenario(dropped_wallet_46, scenario(dropped_wallet, false, true, isolated_area, law_posted, false)).
scenario(dropped_wallet_47, scenario(dropped_wallet, false, true, isolated_area, unclear, true)).
scenario(dropped_wallet_48, scenario(dropped_wallet, false, true, isolated_area, unclear, false)).
scenario(dropped_wallet_49, scenario(dropped_wallet, false, false, many_people_around, none, true)).
scenario(dropped_wallet_50, scenario(dropped_wallet, false, false, many_people_around, none, false)).
scenario(dropped_wallet_51, scenario(dropped_wallet, false, false, many_people_around, cctv_visible, true)).
scenario(dropped_wallet_52, scenario(dropped_wallet, false, false, many_people_around, cctv_visible, false)).
scenario(dropped_wallet_53, scenario(dropped_wallet, false, false, many_people_around, law_posted, true)).
scenario(dropped_wallet_54, scenario(dropped_wallet, false, false, many_people_around, law_posted, false)).
scenario(dropped_wallet_55, scenario(dropped_wallet, false, false, many_people_around, unclear, true)).
scenario(dropped_wallet_56, scenario(dropped_wallet, false, false, many_people_around, unclear, false)).
scenario(dropped_wallet_57, scenario(dropped_wallet, false, false, isolated_area, none, true)).
scenario(dropped_wallet_58, scenario(dropped_wallet, false, false, isolated_area, none, false)).
scenario(dropped_wallet_59, scenario(dropped_wallet, false, false, isolated_area, cctv_visible, true)).
scenario(dropped_wallet_60, scenario(dropped_wallet, false, false, isolated_area, cctv_visible, false)).
scenario(dropped_wallet_61, scenario(dropped_wallet, false, false, isolated_area, law_posted, true)).
scenario(dropped_wallet_62, scenario(dropped_wallet, false, false, isolated_area, law_posted, false)).
scenario(dropped_wallet_63, scenario(dropped_wallet, false, false, isolated_area, unclear, true)).
scenario(dropped_wallet_64, scenario(dropped_wallet, false, false, isolated_area, unclear, false)).



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

rule_sources(Scenario, Action, Sources) :-
    findall(R, (
        (utilitarian_rule(Scenario, Action), R = utilitarian);
        (deontological_rule(Scenario, Action), R = deontological);
        (self_interest_rule(Scenario, Action), R = self_interest)
    ), Sources).



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

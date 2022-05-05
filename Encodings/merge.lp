% Merges single agent plans and detects conflicts.

%% CONFLICT DETECTION %%
v_conflict(RID, RID', NID, T) :- robot_at(RID, NID, T), robot_at(RID', NID, T), RID < RID'.

first_conflict(M) :-  M = #min {T : v_conflict(_, _, _, T)}.

%% REPLAN %%
final_plan(RID, NID, T) :- robot_at(RID, NID, T), first_conflict(M), T < M.

1 { move_alt(RID,D,T) : direction(D) } 1 :- robot(RID), step(T), first_conflict(M), T < M.

final_plan(RID,NID,T) :- move_alt(RID,D,T), final_plan(RID,NID',T-1), nextto(NID',D,NID).

%% GOAL %%
:- not final_plan(_, NID, horizon), goal (NID).

%% AVOID CONFLICTS %%
 :- final_plan(RID,NID,T), final_plan(RID',NID,T), RID < RID'.

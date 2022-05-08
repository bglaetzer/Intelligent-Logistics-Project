% Merges single agent plans and detects conflicts.

%% CONFLICT DETECTION %%
conflict(RID, RID', T) :- robot_at(RID, NID, T), robot_at(RID', NID, T), RID < RID'.
conflict(RID, RID', T) :- robot_at(RID, NID, T), robot_at(RID, NID', T+1), robot_at(RID', NID', T), robot_at(RID', NID, T+1), RID < RID'. 

first_conflict(T) :-  conflict(_, _, T), #false : conflict(_,_,T'), T' < T.

step_re(T) :- step(T), first_conflict(M), T >= M.

%% REPLAN %%
final_plan(RID, NID, T) :- robot_at(RID, NID, T), first_conflict(M), T < M.

{ move_alt(RID,D,T) : direction(D) } 1 :- robot(RID), step_re(T).

int_plan(RID,NID,M-1) :- final_plan(RID,NID,M-1), first_conflict(M).

int_plan(RID,NID,T) :- move_alt(RID,D,T), int_plan(RID,NID',T-1), nextto(NID',D,NID).

%% GOAL %%
:- not final_plan(RID, NID, _), goal(NID, RID).

%% AVOID CONFLICTS %%
:- int_plan(RID,NID,T), int_plan(RID',NID,T), RID < RID'.
:- int_plan(RID, NID, T), int_plan(RID, NID', T+1), int_plan(RID', NID', T), int_plan(RID', NID, T+1), RID < RID'.

final_plan(RID,NID,T) :- int_plan(RID,NID,T).

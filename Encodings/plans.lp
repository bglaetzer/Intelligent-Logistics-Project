% Computes single agent paths for each agent (no conflict detection here).

%#const horizon = 25.
step(1..horizon).

%% INITIAL POSITIONS %%
robot_at(RID, NID, 0) :- robot_at(RID, NID).

%% CONNECTED NODES %%
direction((X,Y)) :- X=-1..1, Y=-1..1, |X+Y|=1.
nextto(ID,(X',Y'),ID') :- node(ID,X,Y), direction((X',Y')), node(ID',X+X',Y+Y').

%% MOVEMENT %%

{ move(RID,D,T) : direction(D) } 1 :- robot(RID), step(T).

robot_at(RID,NID,T) :- move(RID,D,T), robot_at(RID,NID',T-1), nextto(NID',D,NID).

%% GOAL %%
:- not robot_at(RID, NID, _), goal(NID, RID).

%% CONFLICTS %%
conflict(0, RID, RID', NID, T) :- robot_at(RID ,NID, T), robot_at(RID', NID, T), RID < RID'.
conflict(1, RID, RID', (NID, NID'), T) :- robot_at(RID, NID, T), robot_at(RID, NID', T+1), robot_at(RID', NID', T), robot_at(RID', NID, T+1), RID < RID'.

%% MINIMIZATION %%
plan_length(RID, T) :- robot_at(RID,NID,T), goal(NID, RID), robot_at(RID,NID',T-1), not goal(RID, NID').
sum_of_costs(SOC) :- SOC = #sum { T,RID : plan_length(RID, T), robot(RID)}.
#minimize{SOC : sum_of_costs(SOC)}.

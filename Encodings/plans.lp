% Computes single agent paths for each agent (no conflict detection here).

#const horizon = 25.
step(1..horizon).

%% INITIAL POSITIONS %%
robot_at(RID, NID, 0) :- robot_at(RID, NID).

%% CONNECTED NODES %%
direction((X,Y)) :- X=-1..1, Y=-1..1, |X+Y|=1.
direction((0,0)).
nextto(ID,(X',Y'),ID') :- node(ID,X,Y), direction((X',Y')), node(ID',X+X',Y+Y').

%% MOVEMENT %%

 { move(RID,D,T) : direction(D) } 1 :- robot(RID), step(T).

robot_at(RID,NID,T) :- move(RID,D,T), robot_at(RID,NID',T-1), nextto(NID',D,NID).

%% GOAL %%
:- not robot_at(RID, NID, _), goal(NID, RID).

%% MINIMIZATION %%
plan_length(RID, T) :- robot_at(RID,NID,T), goal(NID, RID), #false : robot_at(RID,NID,T'), T' < T.
sum_of_cost(S) :- S = #sum{T,RID : plan_length(RID, T)}.
#minimize{T : sum_of_cost(T)}.
#show robot_at/3.

%To suppress some output
constraint(0,0,0).
% Transforms output into asprilo format
% Truncate last line so it runs with the asprilo-visualizer.

occurs(object(robot, RID), action(move, (X2-X, Y2-Y)), T) :- robot_at(RID,NID2,T+1), node(NID2, X2, Y2), robot_at(RID,NID,T), node(NID, X, Y).
#show.
#show occurs/3.
% Transforms output into asprilo format
% Truncate last line so it runs with the asprilo-visualizer.

occurs(object(robot, ID), action(move, (X2-X, Y2-Y)), T) :- final_plan(ID, V2, T+1), node(V2, X2, Y2), final_plan(ID, V, T), node(V, X, Y).
#show.
#show occurs/3.
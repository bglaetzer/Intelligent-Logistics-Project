% Transforms asprilo inout into a human readable encoding.

% Nodes
node(ID,X,Y) :- init(object(node,ID),value(at,(X,Y))).
node(ID) :- node(ID,_,_).

% Agents
robot_at(R, ID) :- node(ID,X,Y), init(object(robot,R), value(at,(X,Y))).
robot(R) :- robot_at(R, _).

% Goals
goal(ID, SID) :- node(ID,X,Y), init(object(shelf,SID),value(at,(X,Y))).

#show node/3.
#show robot_at/2.
#show goal/2.
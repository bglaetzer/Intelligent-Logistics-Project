% Transforms asprilo inout into a human readable encoding.

% Nodes
node(ID,X,Y) :- init(object(node,ID),value(at,(X,Y))).
node(ID) :- node(ID,_,_).

% Agents
robot_at(R, ID) :- node(ID,X,Y), init(object(robot,R), value(at,(X,Y))).
robot(R) :- robot_at(R, _).

% Goals
goal(ID) :- node(ID,X,Y), init(object(shelf,_),value(at,(X,Y))).
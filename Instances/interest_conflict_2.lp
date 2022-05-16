%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Grid size X: 7
%Grid size Y: 2
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#program base.

%init
init(object(node, 1), value(at, (1, 1))).
init(object(node, 2), value(at, (2, 1))).
init(object(node, 3), value(at, (3, 1))).
init(object(node, 4), value(at, (4, 1))).
init(object(node, 5), value(at, (5, 1))).
init(object(node, 6), value(at, (6, 1))).
init(object(node, 7), value(at, (7, 1))).
init(object(node, 8), value(at, (1, 2))).
init(object(node, 9), value(at, (2, 2))).
init(object(node, 13), value(at, (6, 2))).
init(object(node, 14), value(at, (7, 2))).


init(object(robot,2), value(at,(1,2))).
init(object(robot,1), value(at,(2,2))).
%init(object(robot,1), value(max_energy,X)).
%init(object(robot,1), value(energy,X)).
init(object(shelf,2), value(at,(6,2))).
%init(object(product,0),value(on,(X,X))).
init(object(shelf,1), value(at,(6,1))).

% Clingraph visualization script
% Entirely by Jan Behrens

#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")

def join(base,*args):
    return String(str(base).strip('"').join([str(x).strip('"') for x in args]))
#end.

%position(shelf(S),P,T) :- position(shelf(S),P,0), time(T).
move(robot(R),(X,Y),T) :- occurs(object(robot,R),action(move,(X,Y)),T).
position(shelf(S),P,T) :- init(object(shelf,S), value(at,P)), time(T).
position(robot(R),P,0) :- init(object(robot,R), value(at,P)).
position(P)            :- init(object(node ,_), value(at,P)).

time(T) :- move(_,_,T).
time(T-1) :- time(T), T>0.

% - move/3 ----------------------------------------------------------------------
position(robot(R),(X+DX,Y+DY),T) :- move(robot(R),(DX,DY),T), position(robot(R),(X,Y),T-1).

% - inertia ---------------------------------------------------------------------
position(robot(R),C,T) :- position(robot(R),C,T-1), not move(robot(R),_,T), time(T).

% One graph per time
graph(T) :- time(T).
graph(0).
attr(graph, G, label,   "")      :- graph(G).
attr(graph, G, style,   invis)   :- graph(G).
attr(graph, G, type,    digraph) :- graph(G).
attr(graph, G, nodesep, 1)       :- graph(G).
attr(graph, G, newrank, true)    :- graph(G).

% Global node/edge attributes
attr(graph_nodes, G, width,     "0.5")    :- graph(G).
attr(graph_nodes, G, height,    "0.5")    :- graph(G).
attr(graph_nodes, G, fixedsize, "shape")  :- graph(G).
attr(graph_nodes, G, fontsize,  "8")      :- graph(G).
attr(graph_nodes, G, style,     "filled") :- graph(G).
attr(graph_edges, G, shape,     vee)      :- graph(G).
attr(graph_edges, G, style,     dotted)   :- graph(G).
attr(graph_edges, G, arrowsize, "0.5")    :- graph(G).

% Movements as edges
edge(((X,Y,T),(X+DX,Y+DY,T)),T) :- move(robot(R),(DX,DY),T), position(robot(R),(X,Y),T-1).

size(X,Y):- #max{X':position((X',Y'))}=X, #max{Y':position((X',Y'))}=Y.
% One node per position
node((X,Y,T),T) :- position((X,Y)), time(T).
attr(node, (X,Y,T),pos,@pos(X,YMax-Y)) :- position((X,Y)), time(T), size(XMax,YMax).

% Shape
attr(node, (X,Y,T),shape,"circle") :- position(robot(R),(X,Y),T), not position(shelf(_),(X,Y),T).
attr(node, (X,Y,T),shape,"box")    :- position(shelf(S),(X,Y),T), not position(robot(_),(X,Y),T).
attr(node, (X,Y,T),shape,"square") :- position(shelf(S),(X,Y),T), position(robot(R),(X,Y),T).
attr(node, (X,Y,T),shape,"point")  :- node((X,Y,T),T), not position(_,(X,Y),T).

% Label
attr(node, (X,Y,T),label,"") :- node((X,Y,T),T), not position(_,(X,Y),T).
attr(node, (X,Y,T),label,@join("","R",R)) :- {position(robot(_),(X,Y),T)}=1, not position(shelf(_),(X,Y),T), position(robot(R),(X,Y),T).
attr(node, (X,Y,T),label,@join("","S",S)) :- position(shelf(S),(X,Y),T), not position(robot(_),(X,Y),T).

% Robot and shelf
attr(node, (X,Y,T),label,@join("","R",R,"   ","S",S)) :- position(shelf(S),(X,Y),T), position(robot(R),(X,Y),T).

%% Two robots
attr(node, (X,Y,T),(label,0),@join("","R",R)) :- position(robot(R),(X,Y),T), position(robot(R2),(X,Y),T), R<R2.
attr(node, (X,Y,T),(label,1),@join("","R",R2)) :- position(robot(R),(X,Y),T), position(robot(R2),(X,Y),T), R<R2.
attr(node, (X,Y,T),(label,sep),"\n") :- position(robot(R),(X,Y),T), position(robot(R2),(X,Y),T), R<R2.

% Fillcolor
attr(node, (X,Y,T),fillcolor,@join("","/blues9/",1+R)) :- {position(robot(_),(X,Y),T)}=1, not position(shelf(_),(X,Y),T), position(robot(R),(X,Y),T).
attr(node, (X,Y,T),fillcolor,@join("","/orrd9/", 1+S)) :- position(shelf(S),(X,Y),T), not position(robot(_),(X,Y),T).
attr(node, (X,Y,T),fillcolor,@join("","/blues9/",1+R,":","/blues9/",1+R2)) :- position(robot(R),(X,Y),T), position(robot(R2),(X,Y),T), R<R2.
attr(node, (X,Y,T),fillcolor,@join("","/blues9/",1+R,":","/orrd9/", 1+S))  :- position(shelf(S),(X,Y),T), position(robot(R ),(X,Y),T).
attr(node, (X,Y,T),    color,white) :- position((X,Y)), not position(_,(X,Y),T), time(T).
attr(node, (X,Y,T),fillcolor,black) :- position((X,Y)), not position(_,(X,Y),T), time(T).

% Penwidth
attr(node, (X,Y,T),penwidth,30):- position((X,Y)), not position(_,(X,Y),T), time(T).

% Style
attr(node, (X,Y,T),style,"wedged")  :- position(robot(R),(X,Y),T), position(robot(R2),(X,Y),T), R<R2.
attr(node, (X,Y,T),style,"striped") :- position(shelf(S),(X,Y),T), position(robot(R ),(X,Y),T).
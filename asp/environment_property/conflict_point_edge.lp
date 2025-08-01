conflict_point_edge(train(ID1),D,(X0,Y0),(X1,Y1)) :-
    delta(train(ID1),(X0,Y0),_),
    delta(train(ID1),(X1,Y1),D), 
    (X0,Y0) != (X1,Y1), X0 <= X1, Y0 <= Y1,
    position(train(ID1),(X0,Y0),_,T0),
    action(train(ID1),_,T0),
    position(train(ID1),(X1,Y1),_,T1),
    T1 = T0 + 1.
conflict_point_edge(train(ID1),D,(X0,Y0),(X1,Y1)) :-
    delta(train(ID1),(X1,Y1),_),
    delta(train(ID1),(X0,Y0),D), 
    (X0,Y0) != (X1,Y1), X0 <= X1, Y0 <= Y1,
    position(train(ID1),(X1,Y1),_,T0),
    action(train(ID1),_,T0),
    position(train(ID1),(X0,Y0),_,T1),
    T1 = T0 + 1.

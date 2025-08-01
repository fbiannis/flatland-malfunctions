delta_conflict_point_edge(train(ID1),train(ID2),D1,D2,(X0,Y0),(X1,Y1)) :-
    conflict_point_edge(train(ID1),D1,(X0,Y0),(X1,Y1)),
    conflict_point_edge(train(ID2),D2,(X0,Y0),(X1,Y1)),
    ID1 < ID2.

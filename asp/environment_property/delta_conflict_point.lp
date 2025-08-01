delta_conflict_point(train(ID1),train(ID2),D1,D2,(X,Y)) :-
    conflict_point(train(ID1),train(ID2),(X,Y)),
    delta(train(ID1),(X,Y),D1),
    delta(train(ID2),(X,Y),D2).

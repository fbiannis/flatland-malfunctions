conflict_point(train(ID1),train(ID2),(X,Y)) :-
    ID1 < ID2,
    position(train(ID1),(X,Y),_,_),
    position(train(ID2),(X,Y),_,_).


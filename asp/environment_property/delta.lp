delta(train(ID),(X,Y),D) :-
    conflict_point(train(ID),_,(X,Y)),
    position(train(ID),(X,Y),_,D).
delta(train(ID),(X,Y),D) :-
    conflict_point(_,train(ID),(X,Y)),
    position(train(ID),(X,Y),_,D).

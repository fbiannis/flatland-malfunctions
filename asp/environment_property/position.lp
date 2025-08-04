diff(0, -1, 0). % Heading 0:↑ Up
diff(1, 0, 1).  % Heading 1:→ Right
diff(2, 1, 0).  % Heading 2:↓ Down
diff(3, 0, -1). % Heading 3:← Left

%% Position and heading of a train at a given timestep %%

% Translate cell codes to (type, rotation) format
% cell_type(Coord, Type, RotationNr)

cell_type((X,Y), "Straight", 0) :- cell((X,Y), 32800).
cell_type((X,Y), "Straight", 1) :- cell((X,Y), 1025).

cell_type((X,Y), "Curve", 0) :- cell((X,Y), 4608).
cell_type((X,Y), "Curve", 1) :- cell((X,Y), 2064).
cell_type((X,Y), "Curve", 2) :- cell((X,Y), 72).
cell_type((X,Y), "Curve", 3) :- cell((X,Y), 16386).

cell_type((X,Y), "Switch_Left", 0) :- cell((X,Y), 37408).
cell_type((X,Y), "Switch_Left", 1) :- cell((X,Y), 3089).
cell_type((X,Y), "Switch_Left", 2) :- cell((X,Y), 32872).
cell_type((X,Y), "Switch_Left", 3) :- cell((X,Y), 17411).

cell_type((X,Y), "Switch_Right", 0) :- cell((X,Y), 49186).
cell_type((X,Y), "Switch_Right", 1) :- cell((X,Y), 5633).
cell_type((X,Y), "Switch_Right", 2) :- cell((X,Y), 34864).
cell_type((X,Y), "Switch_Right", 3) :- cell((X,Y), 1097).

cell_type((X,Y), "Diamond", 0) :- cell((X,Y), 33825).

cell_type((X,Y), "Diamond_Single_Slip", 0) :- cell((X,Y), 38433).
cell_type((X,Y), "Diamond_Single_Slip", 1) :- cell((X,Y), 35889).
cell_type((X,Y), "Diamond_Single_Slip", 2) :- cell((X,Y), 33897).
cell_type((X,Y), "Diamond_Single_Slip", 3) :- cell((X,Y), 50211).

cell_type((X,Y), "Diamond_Double_Slip", 0) :- cell((X,Y), 38505).
cell_type((X,Y), "Diamond_Double_Slip", 1) :- cell((X,Y), 52275).

cell_type((X,Y), "Switch_Symmetrical", 0) :- cell((X,Y), 20994).
cell_type((X,Y), "Switch_Symmetrical", 1) :- cell((X,Y), 6672).
cell_type((X,Y), "Switch_Symmetrical", 2) :- cell((X,Y), 2136).
cell_type((X,Y), "Switch_Symmetrical", 3) :- cell((X,Y), 16458).

% For waiting
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), wait, T),
    position(train(ID), (X,Y), H,T).

% For straight tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0, Y0), "Straight", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, H = H0.

% For curves going left
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Curve", R),
    R = H0,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+3)\4.

% For curves going right
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Curve", R),
    R = (H0+3)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+1)\4.

% For left switch tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Left", R),
    H0 != (R+1)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, H = H0.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Left", R),
    H0 = (R+1)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+1)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_left, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Left", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+3)\4.

% For right switch tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Right", R),
    H0 != (R+3)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, H = H0.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Right", R),
    H0 = (R+3)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+3)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_right, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Right", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+1)\4.

% For diamond tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, H = H0.

% For single slip diamond tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Single_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = H0.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_left, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Single_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+3)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_right, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Single_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+1)\4.

% For single slip diamond tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Double_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = H0.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_left, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Double_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+3)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_right, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Diamond_Double_Slip", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY,
    H = (H0+1)\4.

% For symmetrical switch tracks
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Symmetrical", R),
    H0 = (R+1)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+1)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_forward, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Symmetrical", R),
    H0 = (R+3)\4,
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+3)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_left, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Symmetrical", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+3)\4.
position(train(ID), (X,Y), H, T+1) :-
    action(train(ID), move_right, T),
    position(train(ID), (X0,Y0), H0, T),
    cell_type((X0,Y0), "Switch_Symmetrical", _),
    diff(H, DiffX, DiffY),
    X = X0+DiffX, Y = Y0+DiffY, 
    H = (H0+1)\4.

%% Initial position of a train at the start of its route
position(train(ID), (X,Y), 0, 0) :-
    start(ID, (X,Y), _, n). % Maybe needs "earliest departure" handling
position(train(ID), (X,Y), 1, 0) :-
    start(ID, (X,Y), _, e). % Maybe needs "earliest departure" handling
position(train(ID), (X,Y), 2, 0) :-
    start(ID, (X,Y), _, s). % Maybe needs "earliest departure" handling
position(train(ID), (X,Y), 3, 0) :-
    start(ID, (X,Y), _, w). % Maybe needs "earliest departure" handling
    
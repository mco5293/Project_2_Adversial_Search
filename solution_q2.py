import math
def read_input():
    with open('input.txt',"r") as file: #open and read all of input.txt
        input = file.read()
        
    if not input: #make sure input is not empty
        return "Empty input" #input was empty

    else: 
        input=input.strip()
        input = input.replace("\n",",")#replace newlines so it can all be split by commas
        input = input.split(",") #separate by comma, 1d array

        for j in range(len(input)): #make them ints so we can perform operations on them later
            input[j] = int(input[j])

        board=[]#2d 6x6 array
        for i in range(0,36,6): #count by 6 for each row
            board.append(input[i:i+6]) #append the 6 numbers in row to board array, makes a whole row in the 2d array
        return board

#print(read_input())

def apply_move(state_space,move,player_turn):
    new_state = []
    for row in state_space:
        new_state.append(row[:])

    i=move[0]
    j=move[1]
    move_type = move[2]
    new_state[i][j] = player_turn

    if move_type=="TA":
        if i<5 and state_space[i+1][j] not in (player_turn,"U"):
            new_state[i+1][j] = player_turn
        if i >0 and state_space[i-1][j] not in (player_turn,"U"):
            new_state[i-1][j] = player_turn
        if j <5 and state_space[i][j+1] not in (player_turn,"U"):
            new_state[i][j+1] = player_turn
        if j >0 and state_space[i][j-1] not in (player_turn,"U"):
            new_state[i][j-1] = player_turn
def minimax(board,state_space,player_turn,depth):   
    sd_moves = [] #format is tuple where i and j are indicies and SD or TA for type of move and then last space is for N,E,S,W move or U if S.D

    #find all possible moves for unoccupied tiles for STRATEGIC DEPLOYMENT
    for i in range(6):
        for j in range(6):
            if state_space[i][j]=="U":
                sd_moves.append((i,j,"SD","U"))
    
    #find all of Alpha's occupied tiles
    alpha_score = 0
    alpha_tiles = []
    for i in range(6):
        for j in range(6):
            if state_space[i][j]=="A":
                alpha_score += board[i][j]
                alpha_tiles.append((i,j))

    #find all of Bravo's occupied tiles
    bravo_tiles = []
    bravo_score = 0
    for i in range(6):
        for j in range(6):
            if state_space[i][j]=="B":
                bravo_score += board[i][j]
                bravo_tiles.append((i,j))

    #BASE CASE
    if depth==0 or len(sd_moves) == 0: #game is over every tile is occupied
        return (alpha_score-bravo_score), None

    opposite_player="A"
    my_tiles = bravo_tiles
    best_score = math.inf #current players score
    if player_turn == "A":
        best_score = -math.inf
        my_tiles = alpha_tiles
        opposite_player = "B"
    best_move = None
    best_scores = None

    #TACTICAL ASSAULT
    ta_moves = []
    for tile in my_tiles: #tile format is (i,j)
        #N, S, E, W
        i = tile[0]
        j = tile[1]

        if(i<5 and state_space[i+1][j]=="U"):
            ta_moves.append((i+1,j,"TA","S")) #SOUTH
        if(i>0 and state_space[i-1][j]=="U"):
            ta_moves.append((i-1,j,"TA","N")) #NORTH
        if(j<5 and state_space[i][j+1]=="U"):
            ta_moves.append((i,j+1,"TA","E")) #EAST
        if(j>0 and state_space[i][j-1]=="U"):
            ta_moves.append((i,j-1,"TA","W")) #WEST

    #combine both types into one list
    all_moves = sd_moves + ta_moves
    for move in all_moves: #move format is (i,j,SD or TA, U or N or W or E or S)
        new_state= [] #copying state space so can find the best move without modifying the actual state space
        for row in state_space:
            new_state.append(row[:])#makes sure it is a copy of the row and not actually modifying the actual state space

        i = move[0]
        j = move[1]
        move_type = move[2]
        direction = move[3]

        if move_type == "SD":
            new_state[i][j] = player_turn
            

        if move_type == "TA":
            new_state[i][j] = player_turn
            if(i<5 and state_space[i+1][j]!=player_turn and state_space[i+1][j]!="U"):
                new_state[i+1][j] = player_turn #SOUTH
            if(i>0 and state_space[i-1][j]!=player_turn and state_space[i-1][j]!="U"):
                new_state[i-1][j] = player_turn #NORTH
            if(j<5 and state_space[i][j+1]!=player_turn and state_space[i][j+1]!="U"):
                new_state[i][j+1] = player_turn #EAST
            if(j>0 and state_space[i][j-1]!=player_turn and state_space[i][j-1]!="U"):
                new_state[i][j-1] = player_turn #WEST

        result = minimax(board,new_state,opposite_player,depth-1)
        #print(result)                
        scores = result[0]
        if player_turn == "A":
            current_score = scores[0]
            if current_score > best_score:
                best_move = move
                best_scores = scores
            best_score = max(best_score,current_score)
        else:
            current_score = scores[1]
            if current_score < best_score:
                best_move = move
                best_scores = scores
            best_score = min(best_score,current_score)

    return best_scores, best_move


def play():
    #WHO OWNS A TILE: 'U' = unoccupied, 'A' = alpha, 'B' = bravo
    state_space = [['U','U','U','U','U','U'],['U','U','U','U','U','U'],['U','U','U','U','U','U']
                   ,['U','U','U','U','U','U'],['U','U','U','U','U','U'],['U','U','U','U','U','U']] #state space will only have who occupies each tile because that is the only thing that changes, its inicies correspond to the board, which the values don't change
    board = read_input()
    result = minimax(board,state_space,"A",2)
    print(f"Best scores: {result[1]}\nBest move: {result[1]}")

play()

    
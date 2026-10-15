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
    return new_state


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
        return alpha_score, None

    opposite_player="A"
    my_tiles = bravo_tiles
    best_score = math.inf #current players score
    if player_turn == "A":
        best_score = -math.inf
        my_tiles = alpha_tiles
        opposite_player = "B"
    best_move = None

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

    #Makes sure the TA moves actually capture an opponent
    valid_ta_moves=[]
    for move in ta_moves:
        new_state = apply_move(state_space,move,player_turn)
        capture=False
        for i in range(6):
            for j in range(6):
                if state_space[i][j] not in ('U',player_turn): #check if it is the opposing player's tile. it cannot be unoccupied
                    if new_state[i][j]==player_turn:#make sure the move allows for the player to capture the tile
                        capture=True
        if capture:#add it to the list of valid tactical assault moves
            valid_ta_moves.append(move)

    #combine both types into one list
    all_moves = sd_moves + valid_ta_moves
    for move in all_moves: #move format is (i,j,SD or TA, U or N or W or E or S)
        new_state = apply_move(state_space,move,player_turn)
        
        result = minimax(board,new_state,opposite_player,depth-1)
        score = result[0]
        #print(result)
        
        if player_turn == "A":
            if score > best_score:
                best_move = move
            best_score = max(best_score,score)
        else:
            if score < best_score:
                best_move = move
            best_score = min(best_score,score)

    return best_score,best_move


def play():
    #WHO OWNS A TILE: 'U' = unoccupied, 'A' = alpha, 'B' = bravo
    state_space = [['U','U','U','U','U','U'],['U','U','U','U','U','U'],['U','U','U','U','U','U']
                   ,['U','U','U','U','U','U'],['U','U','U','U','U','U'],['U','U','U','U','U','U']] #state space will only have who occupies each tile because that is the only thing that changes, its inicies correspond to the board, which the values don't change
    board = read_input()
    player_turn = "A"

    move_num=1
    game_over= False

    while not game_over:#continue until the board is filled up, no unoccupied spaces
        result = minimax(board,state_space,player_turn,2)#run minimax with depth of 2
        best_move=result[1]
        state_space = apply_move(state_space,best_move,player_turn)

        #for row in state_space:
            #print(row)
        alpha_score=0
        bravo_score=0
        #get scores
        for i in range(6):
            for j in range(6):
                if state_space[i][j]=="A":
                    alpha_score+=board[i][j]
                elif state_space[i][j]=="B":
                    bravo_score+=board[i][j]
        print(f"Move {move_num}")
        move_num+=1
        if player_turn=="A":
            print("Minimax action for team: <Team-Alpha>")
        else:
            print("Minimax action for team: <Team-Bravo>")

        print_str="<"
        for i in range(6):
            for j in range(6):
                if j == 5:
                    if i ==5:
                        print_str = print_str + str(board[i][j])
                    else:
                        print_str =print_str + str(board[i][j]) + "\n"
                else:
                    print_str = print_str + str(board[i][j]) + ","
        
        print_str = print_str+">"

        print(print_str)
        print(f"Total score - Alpha: {alpha_score}")
        print(f"Total score - Bravo: {bravo_score}\n\n")
        
        #swicth players
        if player_turn == "A":
            player_turn="B"
        else:
            player_turn = 'A'

        game_over = True
        for i in range(6):
            for j in range(6):
                if state_space[i][j]=='U':
                    game_over = False
    #print winner
    if alpha_score>bravo_score:
        print("The Winner is: <Team-Alpha>")
    elif alpha_score<bravo_score:
        print("The Winner is: <Team-Bravo>")
    else:
            print("The Winner is: <Tie>")

play()
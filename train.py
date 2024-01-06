import numpy as np
import pandas as pd
import pickle
import json
from AgentSARSA import get_board,get_moves,get_state,choose_action,reward,update_qvalue
import copy
import time
from someShitFunctions import reset,display_board,check_termination
with open('q_values.json','r') as file:
    q_values=json.load(file)
board=np.zeros((3, 3),dtype=int)
def is_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False
def find_forks(board, player):
    print("searching for forks :D")
    forks = []
    moves = get_moves(board)
    print(moves)
    for move in moves:
        row, col = move
        board[row][col] = player
        wins = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player
                    if is_winner(board, player):
                        wins += 1
                        #print("win at: "+str(i)+" "+str(j))
                    board[i][j] = 0  # Undo opponent's move
        #print(str(row)+" "+str(col)+" wins:"+str(wins))
        if wins > 1:
            forks.append(move)

        board[row][col] = 0  # Undo the move
    
    return forks
def move_teacher(board,epsilon):
    global q_values
    board_copy=copy.deepcopy(board)
    moves=get_moves(board_copy)
    x=np.random.rand()
    move = None  # Initialize move variable
    if(x>epsilon):
        for m in moves:
            row, col = m
            board_copy[row][col] = 1
            if is_winner(board_copy, 1):
                print("winning")
                move = m
                break
            board_copy[row][col] = 0  # Undo the move

        # Check for a blocking move (opponent's winning move)
        if move is None:
            for m in moves:
                row, col = m
                board_copy[row][col] = 2
                if is_winner(board_copy, 2):
                    print("blocking")
                    move = m
                    break
                board_copy[row][col] = 0  # Undo the move
                
        # Check for fork opportunities
        if move is None:
            fork_moves = find_forks(board_copy, 1)
            if fork_moves:
                print("fork")
                x2=np.random.rand()
                move = fork_moves[int(x2*len(fork_moves))]  # Store the first fork found

        # If no winning, blocking, or forking move, seize the corners and center
        if move is None:
            corner_moves = [(0, 0), (0, 2), (2, 0), (2, 2)]
            corners_present=[]
            for m in corner_moves:
                if m in moves:
                    corners_present.append(m)
                    print("seizing corner")
            if len(corners_present)!=0:
                x3=np.random.rand()        
                move = corners_present[int(x3*len(corners_present))]   
                

        if move is None and (1, 1) in moves:
            print("seizing center")
            move = (1, 1)
            

        if move is None:
            x1 = np.random.rand()
            print("no other choice")
            move = moves[int(x1 * len(moves))]
    else:
        x1 = np.random.rand()
        print("random move")
        move = moves[int(x1 * len(moves))]
        
        
    print("move by teacher:",move)
    row,col=move
    '''
    tStatus=check_termination(board,(row,col),1)
    if(tStatus!=-1):
       with open('q_values.json', 'r') as file:
           q_values = json.load(file)
       qValue=q_values.get(str(get_state(board)),0.0)    
       q_values[str(get_state(board))]=(qValue+0.1*(reward(board,(row,col),1)-qValue))    
       with open('q_values.json','w') as file:
           json.dump(q_values,file,indent=4)
    '''
    board[row][col]=1
        
    
def move_agent(board,epsilon):
    global q_values
    board_copy=copy.deepcopy(board)
    move=choose_action(board_copy,epsilon) 
    row,col=move
    board[row][col]=2
    
    
    

start_time = time.time()
teacher_win=0
agent_win=0
draws=0
iterations=10
teacher_epsilon_initial=0
teacher_epsilon=0
agent_epsilon=0
alpha=0.02
gamma=1
for i in range(iterations):
    a=None
    a_prev=None    
    board_prev=None
    if (i+1) % 100 == 0:
        elapsed_time = time.time() - start_time
        start_time=time.time()
        print(f"{i+1} baar khel chuka Agent Smith uWu. Elapsed time: {elapsed_time:.2f} seconds")
    print("game started",i)
    board=np.zeros((3, 3),dtype=int)
    move_teacher(board,teacher_epsilon_initial)
    reset(board)
    while(True):
        move_agent(board,agent_epsilon)
        a=get_state(board)
        
        
        if a_prev is not None:
            with open('q_values.json','r') as file:
                q_values=json.load(file)
            qValueA_prev=q_values.get(str(a_prev),0.0)
            qValueA=q_values.get(str(a),0.0)
            qValueA_prev=qValueA_prev+alpha*(reward(board_prev)+gamma*qValueA-qValueA_prev)
            q_values[str(a_prev)]=qValueA_prev
            with open('q_values.json','w') as file:
                q_values=json.dump(q_values,file,indent=4)    
            if(check_termination(board)==2):
                with open('q_values.json','r') as file:
                    q_values=json.load(file)
                qValueA=q_values.get(str(a),0.0)
                qValueA=qValueA+alpha*(reward(board)-qValueA)
                q_values[str(a)]=qValueA
                with open('q_values.json','w') as file:
                    q_values=json.dump(q_values,file,indent=4)
                agent_win+=1
                break
                
        board_prev=copy.deepcopy(board)      
        move_teacher(board,teacher_epsilon) 

        if check_termination(board)==1 or check_termination(board)==0:
            if(check_termination(board)==1):
                teacher_win+=1
            else:
                draws+=1
            
            if a_prev is not None:
                with open('q_values.json','r') as file:
                    q_values=json.load(file)
                qValueA=q_values.get(str(a),0.0)
                qValueA=qValueA+alpha*(reward(board)-qValueA)
                q_values[str(a)]=qValueA
                with open('q_values.json','w') as file:
                    q_values=json.dump(q_values,file,indent=4)
                break;    
        a_prev=a    
print("Teacher wins:",teacher_win)
print("agent wins: ", agent_win)
print("Draws: ",draws)           
            
            
            
            
        
                
            
    
    
    

import numpy as np
import pandas as pd
import pickle
import json
import copy
from someShitFunctions import check_termination,reset
def get_moves(board):
    moves=[]
    for i in range(3):
        for j in range(3):
            if(board[i][j])==0:
                moves.append((i,j))
    return moves
def get_state(board,move=None,player=2):
    board_copy = copy.deepcopy(board)
    if move is not None:
        row,col=move
        board_copy[row][col]=player
    return tuple(map(tuple,board_copy))
def get_board(board,move=None,player=2):
    if move is not None:
        row,col=move
    board_copy = copy.deepcopy(board)
    board_copy[row][col]=player
    return board_copy
    
def choose_action(board,epsilon=1):
    moves=get_moves(board)
    print("moves possible:")
    print(moves)
    print("board before bot move")
    print(board)
    x=np.random.rand(1)
    maxAfterstateAction=();
    q_values={}
    with open('q_values.json', 'r') as file:
        q_values = json.load(file)
        #print("Loaded Q values:", q_values)
    max=-1000     #no value could possibly be lower than -1000
    if(x<epsilon):
        x1=np.random.rand(1)
        print("random move")
        print(moves[int(x1*len(moves))])
        return moves[int(x1*len(moves))]
        
    else:
       '''
       iterate through the 'moves' and get the afterstate for them 
       and then find the one with the maximum Q-value and return that 
       move
       '''
       for move in moves:
           if q_values.get(str(get_state(board,move))) is None:
               q_values[str(get_state(board,move))]=0.0
           if(q_values.get(str(get_state(board,move)))>max):
               maxAfterstateAction=move
               max=q_values.get(str(get_state(board,move)))       
       print("chosen move:"+str(maxAfterstateAction))        
       print("chosen afterstate:"+str(get_state(board,maxAfterstateAction))+str(max))        
       return maxAfterstateAction
def update_qvalue(board,move,alpha,gamma,player):
    board_copy=copy.deepcopy(board)
    with open('q_values.json', 'r') as file:
        q_values = json.load(file)
    afterstate1=get_state(board_copy,None,player)
    afterstate2=get_state(board_copy,move,player)
    q_value1 = q_values.get(str((afterstate1)), 0.0)
    q_value2 = q_values.get(str((afterstate2)), 0.0)
    tStatus=check_termination(board_copy,move)
    if tStatus!=-1:
        q_value2=0   
    ''' 
    if(check_termination(get_board(board,move))==-1):
        q_value1= q_value1 + alpha*(reward(board,move) + q_value2*gamma - q_value1)
    else:
        q_value1= q_value1 + alpha*(reward(board,move) - q_value1)
        q_values[afterstate2]=0.0
        '''
    q_value1= q_value1 + alpha*(reward(board_copy,move) + q_value2*gamma - q_value1)
    q_values[str((afterstate1))]=q_value1   
    with open('q_values.json', 'w') as file:
        json.dump(q_values, file,indent=4)
    if(tStatus!=-1):
        reset(board)
def reward(board,move=None,player=2):
    board_copy=copy.deepcopy(board)
    if(move!=None):
        i,j=move
        board_copy[i][j]=player
    t=check_termination(board_copy)
    if t==1:
        print("reward -10 for the the afterstate")
        print(get_state(board))
        return -10
    elif t==2:
        print("reward +10 for the the afterstate")
        print(get_state(board))
        return 10
    elif t==0:
        print("reward 5 for the the afterstate")
        print(get_state(board))
        return 5
    elif t==-1:
        print("reward 0 for the the afterstate")
        print(get_state(board))
        return 0
    
    
        
    
    
    
           
    

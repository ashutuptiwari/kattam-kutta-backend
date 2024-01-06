import numpy as np
import pandas as pd
import copy
def get_state(board):
    state = tuple(map(tuple, board))
    return state
def display_board(board):
    #prints the current board
    #0 is empty square, 1 is by player 1 , 2 by player 2
    print("Current board")
    '''
    for i in range(3):
        for j in range(3):
            print(f"{board[i][j]} ",end="")
        print()
    '''
    print(get_state(board))    
def check_termination(board,move=None,player=None):
    #0 for draw, 1 if player1 wins, 2 if player2 wins,-1 otherwise
    board_copy=copy.deepcopy(board)
    if move is not None and player is not None:
        i,j=move
        board_copy[i][j]=player
    sum=0    
    for i in range(3):
        for j in range(3):
            sum+=board_copy[i][j]
    for i in range(3):
        if board_copy[i][0]==board_copy[i][1]==board_copy[i][2]==1 or board_copy[0][i]==board_copy[1][i]==board_copy[2][i]==1:
            return 1
        elif board_copy[i][0]==board_copy[i][1]==board_copy[i][2]==2 or board_copy[0][i]==board_copy[1][i]==board_copy[2][i]==2:
            return 2
    if board_copy[0][0]==board_copy[1][1]==board_copy[2][2]==1 or board_copy[2][0]==board_copy[1][1]==board_copy[0][2]==1:
        return 1
    if board_copy[0][0]==board_copy[1][1]==board_copy[2][2]==2 or board_copy[2][0]==board_copy[1][1]==board_copy[0][2]==2:
        return 2
    if(sum==13 or sum==14):
        return 0
    return -1
def reset(board):
    #resets the board
    board=np.zeros((3,3),dtype=int)
    return board
def new_move_dummy(board):
    #dummy move which returns the first empty square, just for checking implementation
    for i in range(3):
        for j in range(3):
            if board[i][j]==0:
                board[i][j]=2
                display_board(board)
                return i,j    
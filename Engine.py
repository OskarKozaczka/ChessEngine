import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from utility import IsKingInCheck, ListEveryLegalMove
from copy import deepcopy
from time import time

def normalize(board):
    pieces=['bp','br','bb','bn','bq','bk','wp','wr','wb','wn','wq','wk']
    sol=[]
    for piece in pieces:
        BinaryBoard=[[0 for i in range(8)] for i in range(8)]
        for row in range(8):
             for square in range(8):
                 if board[row][square]==piece: BinaryBoard[row][square]=1
    
        sol.append(BinaryBoard)
    return sol
                 

model=tf.keras.models.load_model('Data/Data')
Counter=1

def EvaluateBestMove(ChessBoard,WhiteToMove,Castle):
    global Counter
    global model
    if Counter%100==0: model=tf.keras.models.load_model('Data/Data')
    Counter+=1
    t1=time()
    LegalMoves=ListEveryLegalMove(ChessBoard,WhiteToMove,Castle)
    MovesValues={}
    for move in LegalMoves:
        ChessBoardAfterMove=deepcopy(ChessBoard)
        ChessBoardAfterMove[move[2][1]][move[2][0]]=move[0]
        ChessBoardAfterMove[move[1][1]][move[1][0]]='  '
        #check for mate in one
        if len(ListEveryLegalMove(ChessBoardAfterMove,False if WhiteToMove else True,Castle))==0 and IsKingInCheck(ChessBoardAfterMove,False if WhiteToMove else True):
            print('mate in one')
            return move
        ChessBoardAfterMove=normalize(ChessBoardAfterMove)
        ChessBoardAfterMove=tf.expand_dims(ChessBoardAfterMove,0)
        Value=model.predict(ChessBoardAfterMove)[0]
        #print(move,Value)
        MovesValues[Value[0]]=move
        
    BestKey=max(MovesValues.keys()) if WhiteToMove else min(MovesValues.keys())
    print('Evaulation in ',time()-t1)
    return MovesValues[BestKey]
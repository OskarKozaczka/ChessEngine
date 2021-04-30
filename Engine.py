import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from utility import ListEveryLegalMove
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

def EvaluateBestMove(ChessBoard,WhiteToMove):
    t1=time()
    #model=tf.keras.models.load_model('Data/Data')
    LegalMoves=ListEveryLegalMove(ChessBoard,WhiteToMove)
    MovesValues={}
    for move in LegalMoves:
        ChessBoardAfterMove=deepcopy(ChessBoard)
        ChessBoardAfterMove[move[2][1]][move[2][0]]=move[0]
        ChessBoardAfterMove[move[1][1]][move[1][0]]='  '
        #print(array(ChessBoardAfterMove))
        ChessBoardAfterMove=normalize(ChessBoardAfterMove)
        ChessBoardAfterMove=tf.expand_dims(ChessBoardAfterMove,0)
        Value=model.predict(ChessBoardAfterMove)[0]
        #print(Value)
        MovesValues[Value[0]]=move
    BestKey=max(MovesValues.keys()) if WhiteToMove else min(MovesValues.keys())
    print('Evaulation in ',time()-t1)
    return MovesValues[BestKey]
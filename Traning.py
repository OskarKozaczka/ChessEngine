import os
import stockfish
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from utility import ToPositionInFENNotation
from stockfish import Stockfish
from time import time
import tensorflow.keras.callbacks as callbacks

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
                 

stockfish=Stockfish("./stockfish_13/stockfish_13")
stockfish.set_depth(1)
model=tf.keras.models.load_model('Data/Data')

def Train(ChessBoard,WhiteToMove):
    t1=time()
    global model
    #model=tf.keras.models.load_model('Data/Data')
    fen_position=ToPositionInFENNotation(ChessBoard,WhiteToMove)
    stockfish.set_fen_position(fen_position)
    info=stockfish.get_evaluation()
    if info["type"]=="mate": info=10000 if WhiteToMove else -10000
    else: info=info['value']
    ChessBoard=normalize(ChessBoard)
    model.fit([ChessBoard], [info], epochs=1000,verbose=1 ,callbacks=[callbacks.EarlyStopping(monitor='loss', patience=50, min_delta=1e-4)])
    model.save('Data/Data')
    print('Training in ',time()-t1)

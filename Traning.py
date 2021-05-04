import os
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
                 
#To use traning function u have to have stockfish installed in this directory
stockfish=Stockfish("./stockfish_13/stockfish_13") 
stockfish.set_depth(1)
model=tf.keras.models.load_model('Data/Data')

#fen_position='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#stockfish.set_fen_position(fen_position)
#print(stockfish.get_evaluation())

round=1
def Train(ChessBoard,WhiteToMove,Castle):
    global round
    round+=1
    t1=time()
    global model
    fen_position=ToPositionInFENNotation(ChessBoard,WhiteToMove,Castle)
    stockfish.set_fen_position(fen_position)
    info=stockfish.get_evaluation()
    if info["type"]=="mate": print('mate in',info['value'])
    else: 
        info=info['value']
        print(info)
        ChessBoard=normalize(ChessBoard)
        model.fit([ChessBoard], [info], epochs=1,verbose=0 ,callbacks=[callbacks.EarlyStopping(monitor='loss', patience=10, min_delta=1)])
    if round%1000==0:
         model.save('Data/Data')
         print("saved")
    #print('Training in ',time()-t1)

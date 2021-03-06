import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
from utility import IsKingInCheck, ListEveryLegalMove,ToPositionInFENNotation
from copy import deepcopy
from time import time
from Chess import ChessBoard
from stockfish import Stockfish
from statistics import mean
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


def Search(depth,alpha,beta,MaxPlayer):

    if MaxPlayer:
        moves = ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)

        if len(moves)==0:
            if ChessBoard.CheckForEndgameConditions=="Mate": return -100000
            if ChessBoard.CheckForEndgameConditions=="Stalemate": return 0

        if depth==0:
            ChessBoardAfterMove=normalize(ChessBoard.Board)
            ChessBoardAfterMove=tf.expand_dims(ChessBoardAfterMove,0)
            Value=model.predict(ChessBoardAfterMove)[0]
            return Value
        for move in moves:
            SBoard,SCastle,SWhiteToMove=deepcopy(ChessBoard.Board),ChessBoard.Castle,ChessBoard.WhiteToMove
            ChessBoard.Move(move)
            Train(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
            Eval=-Search(depth-1,alpha,beta,False)
            ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove

            alpha = max(alpha,Eval)
            if beta<=alpha:
                break
        return alpha
    else:
        moves = ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)

        if len(moves)==0:
            if ChessBoard.CheckForEndgameConditions=="Mate": return -100000
            if ChessBoard.CheckForEndgameConditions=="Stalemate": return 0

        if depth==0:
            ChessBoardAfterMove=normalize(ChessBoard.Board)
            ChessBoardAfterMove=tf.expand_dims(ChessBoardAfterMove,0)
            Value=model.predict(ChessBoardAfterMove)[0]
            return Value
        for move in moves:
            SBoard,SCastle,SWhiteToMove=deepcopy(ChessBoard.Board),ChessBoard.Castle,ChessBoard.WhiteToMove
            ChessBoard.Move(move)
            Train(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
            Eval=-Search(depth-1,alpha,beta,True)
            ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove
 
            beta = min(alpha,Eval)
            if beta>=alpha:
                break
        return beta


def SearchBestMove(depth):
    if ChessBoard.WhiteToMove:
        BestMove=None
        MaxEval=-100000
        moves = ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
        for move in moves:
            SBoard,SCastle,SWhiteToMove=deepcopy(ChessBoard.Board),ChessBoard.Castle,ChessBoard.WhiteToMove
            ChessBoard.Move(move)
            Eval=Search(depth-1,10000,-10000,False)
            if Eval>MaxEval:
                MaxEval=Eval
                BestMove=move
            ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove
        return BestMove
    else:
        BestMove=None
        MinEval=100000
        moves = ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
        for move in moves:
            SBoard,SCastle,SWhiteToMove=deepcopy(ChessBoard.Board),ChessBoard.Castle,ChessBoard.WhiteToMove
            ChessBoard.Move(move)
            Eval=Search(depth-1,-10000,10000,True)
            if Eval<MinEval:
                MinEval=Eval
                BestMove=move
            ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove
        return BestMove

#To use traning function u have to have stockfish installed in this directory
stockfish=Stockfish("./stockfish_13/stockfish_13") 
stockfish.set_depth(1)
model=tf.keras.models.load_model('Data/Data')

accuracy=[]
round=1

def Train(ChessBoard,WhiteToMove,Castle):
    global round
    global model
    round+=1
    fen_position=ToPositionInFENNotation(ChessBoard,WhiteToMove,Castle)
    stockfish.set_fen_position(fen_position)
    info=stockfish.get_evaluation()
    if info["type"]=="mate": print('mate in',info['value'])
    else: 
        info=info['value']
        #print(info)
        ChessBoard=normalize(ChessBoard)
        model.fit([ChessBoard], [info], epochs=1,verbose=0)
        ChessBoard=tf.expand_dims(ChessBoard,0)
        #EvAcc(info,model.predict(ChessBoard)[0][0])
    if round%1000==0:
         model.save('Data/Data')
         model=tf.keras.models.load_model('Data/Data')
         print("saved")

def EvAcc(value1,value2):
    if len(accuracy)>=10000 : accuracy.pop(0)
    else: accuracy.append(abs(value1-value2))
    print(mean(accuracy),len(accuracy))

def EvaluateBestMove():
    t1=time()
    LegalMoves=ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
    MovesValues={}
    for move in LegalMoves:
        SBoard,SCastle,SWhiteToMove=deepcopy(ChessBoard.Board),ChessBoard.Castle,ChessBoard.WhiteToMove
        ChessBoard.Move(move)
        #check for mate in one
        if len(ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle))==0 and IsKingInCheck(ChessBoard.Board,ChessBoard.WhiteToMove):
            print('mate in one')
            ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove
            return move
        ChessBoardAfterMove=normalize(ChessBoard.Board)
        ChessBoardAfterMove=tf.expand_dims(ChessBoardAfterMove,0)
        Train(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle)
        Value=model.predict(ChessBoardAfterMove)[0]
        MovesValues[Value[0]]=move
        ChessBoard.Board,ChessBoard.Castle,ChessBoard.WhiteToMove=SBoard,SCastle,SWhiteToMove

        
    BestKey=max(MovesValues.keys()) if ChessBoard.WhiteToMove else min(MovesValues.keys())
    print('Evaulation in ',time()-t1)
    return MovesValues[BestKey]
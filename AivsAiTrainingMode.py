from numpy import array
from utility import IsThisStalemate,IsKingInCheck,ToPositionInFENNotation,ListEveryLegalMove
from Engine import EvaluateBestMove
from Traning import Train
from copy import deepcopy

#create a board and setup the pieces
def setup():
    global ChessBoard
    ChessBoard=[["  " for i in range(8)] for i in range (8)]
    for x in range(8): 
        ChessBoard[1][x]='bp'
        ChessBoard[6][x]='wp'
    
    Side=['r','n','b','q','k','b','n','r']
    for i in range(8):
        ChessBoard[0][i]='b'+Side[i]
        ChessBoard[7][i]='w'+Side[i]
setup()

def promote(WhiteToMove):
    if WhiteToMove:
        for square in ChessBoard[0]:
            if square =="wp": ChessBoard[0][ChessBoard[0].index(square)]='wq'
    else:
        for square in ChessBoard[7]:
            if square=="bp": ChessBoard[7][ChessBoard[7].index(square)]='bq'
PieceSelectedPos=False
WhiteToMove=True
OneMoveBackChessBoard=False
Mate=False

def debug():
    print(array(ChessBoard),'\n')
    print("Check",IsKingInCheck(ChessBoard,WhiteToMove))
    print(ToPositionInFENNotation(ChessBoard,WhiteToMove))

def EngineMove():
    for move in ListEveryLegalMove(ChessBoard,WhiteToMove):
        board=deepcopy(ChessBoard)
        board[move[2][1]][move[2][0]]=move[0]
        board[move[1][1]][move[1][0]]='  '
        Train(board,False if WhiteToMove else True)
    Move=EvaluateBestMove(ChessBoard,WhiteToMove)
    move=[Move[0],Move[2][0],Move[2][1]]
    
while True:
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove))>0:
        EngineMove()
        promote(WhiteToMove)
        WhiteToMove=False if WhiteToMove else True
        debug()
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove))==0 and IsKingInCheck(ChessBoard,WhiteToMove):
        print("That is Mate")
        setup()
    elif IsThisStalemate(ChessBoard,WhiteToMove):
        print("That is Stalemate")
        setup()


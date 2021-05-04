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

WhiteToMove=True
MoveCount=0
Castle="KQkq"

def Move(ChessBoard,move):
    global Castle
    #move = (bn,[2,4],[3,6])
    ChessBoard[move[2][1]][move[2][0]]=move[0]
    ChessBoard[move[1][1]][move[1][0]]="  "
    promote(WhiteToMove)
    if move[0][1]=='k' and move[1][0]-move[2][0]==-2:
        ChessBoard[move[1][1]][move[1][0]+3]='  '
        ChessBoard[move[1][1]][move[1][0]+1]='wr' if WhiteToMove else 'br'
        Castle=Castle.replace("K",'') if WhiteToMove else Castle.replace("k",'')
    if move[0][1]=='k' and move[1][0]-move[2][0]==2:
        ChessBoard[move[1][1]][move[1][0]-4]='  '
        ChessBoard[move[1][1]][move[1][0]-1]='wr' if WhiteToMove else 'br'
        Castle=Castle.replace("Q",'') if WhiteToMove else Castle.replace("q",'')

    if ChessBoard[7][7]!="wr": Castle=Castle.replace("K",'')
    if ChessBoard[7][0]!="wr": Castle=Castle.replace("Q",'')
    if ChessBoard[0][7]!="br": Castle=Castle.replace("k",'')
    if ChessBoard[0][0]!="br": Castle=Castle.replace("q",'')
    if ChessBoard[7][4]!="wk": 
        Castle=Castle.replace("K",'')
        Castle=Castle.replace("Q",'')
    if ChessBoard[0][4]!="bk":
         Castle=Castle.replace("k",'')
         Castle=Castle.replace("q",'')
    return ChessBoard

def debug():
    print(array(ChessBoard),'\n')
    print("Check",IsKingInCheck(ChessBoard,WhiteToMove))
    print(ToPositionInFENNotation(ChessBoard,WhiteToMove,Castle))
    print(Castle)

def EngineMove():
    global ChessBoard
    global Castle
    CastleS=Castle
    for move in ListEveryLegalMove(ChessBoard,WhiteToMove,Castle):
        board=deepcopy(ChessBoard)
        board=Move(board,move)
        Train(board,False if WhiteToMove else True,Castle)
    Castle=CastleS
    BestMove=EvaluateBestMove(ChessBoard,WhiteToMove,Castle)
    ChessBoard=Move(ChessBoard,BestMove)
  
    
while True:
    print("Move",MoveCount)
    MoveCount+=1
    if MoveCount>300 and WhiteToMove:
        setup()
        MoveCount=0
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove,Castle))>0:
        EngineMove()
        promote(WhiteToMove)
        WhiteToMove=False if WhiteToMove else True
        debug()
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove,Castle))==0 and IsKingInCheck(ChessBoard,WhiteToMove):
        print("That is Mate")
        setup()
        MoveCount=0
    elif IsThisStalemate(ChessBoard,WhiteToMove):
        print("That is Stalemate")
        setup()
        MoveCount=0


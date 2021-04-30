import pygame
from numpy import array
from utility import IsThisStalemate,IsKingInCheck,ToPositionInFENNotation,ListEveryLegalMove
from Engine import EvaluateBestMove

pygame.init()
screen= pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')


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

def backgroundreset():
    ChessBoardColors=[(47, 121, 173),(169, 175, 176)]

    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen,ChessBoardColors[y%2-x%2],(100*x,100*y,100,100))
backgroundreset()

def UpdatePiecePositions():
    Offset=15
    for y in range(8):
        for x in range(8):
            if ChessBoard[x][y]!='  ': 
                Piece=pygame.image.load('Pieces/{}.png'.format(ChessBoard[x][y]))
                screen.blit(Piece,(100*y+Offset,100*x+Offset))


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

def RedCheckSquare():
    if IsKingInCheck(ChessBoard,WhiteToMove):
        PosOfKing=0
        for x in range(8):
            for y in range(8):
                if ChessBoard[y][x]=='wk' and WhiteToMove: PosOfKing=[x,y]
                if ChessBoard[y][x]=='bk' and WhiteToMove ==False: PosOfKing=[x,y]
        pygame.draw.rect(screen,(255,0,0),(100*PosOfKing[0],100*PosOfKing[1],100,100))

def debug():
    print(array(ChessBoard),'\n')
    print("Check",IsKingInCheck(ChessBoard,WhiteToMove))
    print(ToPositionInFENNotation(ChessBoard,WhiteToMove))

def EngineMove():
    Move=EvaluateBestMove(ChessBoard,WhiteToMove)
    ChessBoard[Move[2][1]][Move[2][0]]=Move[0]
    ChessBoard[Move[1][1]][Move[1][0]]='  '


while True:
    pygame.event.pump()
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
    backgroundreset()
    RedCheckSquare()
    UpdatePiecePositions()
    pygame.display.update()
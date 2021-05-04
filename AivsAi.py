import pygame
from numpy import array
from utility import IsThisStalemate,IsKingInCheck,ToPositionInFENNotation,ListEveryLegalMove
from Engine import EvaluateBestMove
from Traning import Train
from copy import deepcopy
from time import sleep

pygame.init()
screen= pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load('./Pieces/bn.png'))

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

WhiteToMove=True
Castle="KQkq"

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
    move=EvaluateBestMove(ChessBoard,WhiteToMove,Castle)
    ChessBoard=Move(ChessBoard,move)

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


MoveCount=0
while True:
    pygame.event.pump()
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
    backgroundreset()
    RedCheckSquare()
    UpdatePiecePositions()
    pygame.display.update()
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove,Castle))==0 and IsKingInCheck(ChessBoard,WhiteToMove):
        print("That is Mate")
        sleep(5)
        MoveCount=0
        setup()
    elif IsThisStalemate(ChessBoard,WhiteToMove):
        print("That is Stalemate")
        sleep(5)
        MoveCount=0
        setup()

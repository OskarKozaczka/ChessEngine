import pygame
from numpy import array
from utility import MoveValidator,IsKingInCheck,ToPositionInFENNotation,ListEveryLegalMove
from Engine import EvaluateBestMove
import copy

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

def DrawLegalMoves():
    for x in range(8):
        for y in range(8):
            if MoveValidator(PieceSelectedPos,[x,y],PieceSelectedType,ChessBoard,WhiteToMove):
                pygame.draw.rect(screen,(255,140,140),(100*x,100*y,100,100))

def debug():
    print(array(ChessBoard),'\n')
    print(PieceSelectedPos,SquareClicked)
    print("Check",IsKingInCheck(ChessBoard,WhiteToMove))
    print(ToPositionInFENNotation(ChessBoard,WhiteToMove))

def EngineMove():
    Move=EvaluateBestMove(ChessBoard,WhiteToMove)
    ChessBoard[Move[2][1]][Move[2][0]]=Move[0]
    ChessBoard[Move[1][1]][Move[1][0]]='  '

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            debug()
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if PieceSelectedPos:
                if MoveValidator(PieceSelectedPos,SquareClicked,PieceSelectedType,ChessBoard,WhiteToMove):
                    move=(PieceSelectedType,PieceSelectedPos,SquareClicked)
                    print('move',move)
                    OneMoveBackChessBoard=copy.deepcopy(ChessBoard)
                    ChessBoard[SquareClicked[1]][SquareClicked[0]]=ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]
                    ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]='  '
                    promote(WhiteToMove)
                    WhiteToMove=False
                    if len(ListEveryLegalMove(ChessBoard,WhiteToMove))>0:
                        EngineMove()
                        promote(WhiteToMove)
                        WhiteToMove=True
                    if len(ListEveryLegalMove(ChessBoard,WhiteToMove))==0 and IsKingInCheck(ChessBoard,WhiteToMove):
                        print("That is Mate")
                    elif len(ListEveryLegalMove(ChessBoard,WhiteToMove))==0:
                        print("That is Stalemate")
                backgroundreset()
                RedCheckSquare()
                PieceSelectedPos=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if ChessBoard[SquareClicked[1]][SquareClicked[0]]!='  ':
                PieceSelectedPos=SquareClicked
                PieceSelectedType=ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]
                backgroundreset()
                DrawLegalMoves()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ChessBoard!=OneMoveBackChessBoard and OneMoveBackChessBoard:
            print ('move undone')
            ChessBoard=OneMoveBackChessBoard
            if WhiteToMove: WhiteToMove=False
            else: WhiteToMove=True
            backgroundreset()
        if event.type == pygame.QUIT:
            pygame.quit()
    UpdatePiecePositions()
    pygame.display.update()
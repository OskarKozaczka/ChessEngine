import pygame
from numpy import array
from utility import MoveValidator,IsKingInCheck,ToPositionInFENNotation,IsThisStalemate
import copy


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
            if MoveValidator(PieceSelectedPos,[x,y],PieceSelectedPosType,ChessBoard,WhiteToMove):
                pygame.draw.rect(screen,(255,140,140),(100*x,100*y,100,100))

def debug():
    print(array(ChessBoard),'\n')
    print(PieceSelectedPos,SquareClicked)
    print("Check",IsKingInCheck(ChessBoard,WhiteToMove))
    print(ToPositionInFENNotation(ChessBoard,WhiteToMove))

def ListEveryLegalMove():
    ListOfMoves=[]
    for xx in range(8):
        for yy in range(8):
            for x in range(8):
                for y in range(8):
                    if MoveValidator([xx,yy],[x,y],ChessBoard[yy][xx],ChessBoard,WhiteToMove):
                        ListOfMoves.append((ChessBoard[yy][xx],[xx,yy],[x,y]))
    return ListOfMoves

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if PieceSelectedPos:
                if MoveValidator(PieceSelectedPos,SquareClicked,PieceSelectedPosType,ChessBoard,WhiteToMove):
                    OneMoveBackChessBoard=copy.deepcopy(ChessBoard)
                    ChessBoard[SquareClicked[1]][SquareClicked[0]]=ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]
                    ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]='  '
                    promote(WhiteToMove)
                    WhiteToMove=False if WhiteToMove else True

                    if len(ListEveryLegalMove())==0 and IsKingInCheck(ChessBoard,WhiteToMove):
                        print("That is Mate")
                    elif IsThisStalemate(ChessBoard,WhiteToMove):
                        print("That is Stalemate")
                backgroundreset()
                RedCheckSquare()
                PieceSelectedPos=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if ChessBoard[SquareClicked[1]][SquareClicked[0]]!='  ':
                PieceSelectedPos=SquareClicked
                PieceSelectedPosType=ChessBoard[PieceSelectedPos[1]][PieceSelectedPos[0]]
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
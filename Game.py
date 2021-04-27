import pygame
from numpy import array
from utility import MoveValidator,IsKingInCheck
import copy

pygame.init()
screen= pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')

white=(255,255,255)
red=(255,0,0)
green=(0,255,0)

#create a board and setup the pieces
ChessBoard=[["  " for i in range(8)] for i in range (8)]
for x in range(8): 
    ChessBoard[1][x]='bp'
    ChessBoard[6][x]='wp'

Side=['r','n','b','q','k','b','n','r']
for i in range(8):
    ChessBoard[0][i]='b'+Side[i]
    ChessBoard[7][i]='w'+Side[i]

#ChessBoard[2][2]='wr'
def backgroundreset():
    screen.fill(white)
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

PieceSelected=False
WhiteToMove=True
OneMoveBackChessBoard=False
KingInCheck=False

def debug():
    print(array(ChessBoard),'\n')
    print(PieceSelected,SquareClicked)
    print(KingInCheck)
    print(IsKingInCheck(ChessBoard,WhiteToMove))

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            debug()
            if PieceSelected:
                if MoveValidator(PieceSelected,SquareClicked,PieceSelectedType,ChessBoard,WhiteToMove,KingInCheck):
                    OneMoveBackChessBoard=copy.deepcopy(ChessBoard)
                    ChessBoard[SquareClicked[1]][SquareClicked[0]]=ChessBoard[PieceSelected[1]][PieceSelected[0]]
                    ChessBoard[PieceSelected[1]][PieceSelected[0]]='  '

                    if WhiteToMove: WhiteToMove=False
                    else: WhiteToMove=True
                    if IsKingInCheck(ChessBoard,WhiteToMove): KingInCheck=True
                    else :KingInCheck=False
                backgroundreset()
                #put a red square on king if he is in check
                if KingInCheck:
                    PosOfKing=0
                    for x in range(8):
                        for y in range(8):
                            if ChessBoard[y][x]=='wk' and WhiteToMove: PosOfKing=[x,y]
                            if ChessBoard[y][x]=='bk' and WhiteToMove ==False: PosOfKing=[x,y]
                    pygame.draw.rect(screen,red,(100*PosOfKing[0],100*PosOfKing[1],100,100))
                PieceSelected=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if ChessBoard[SquareClicked[1]][SquareClicked[0]]!='  ':
                PieceSelected=SquareClicked
                PieceSelectedType=ChessBoard[PieceSelected[1]][PieceSelected[0]]
                backgroundreset()
                #draw all legal moves for selected piece
                for x in range(8):
                    for y in range(8):
                        if MoveValidator(PieceSelected,[x,y],PieceSelectedType,ChessBoard,WhiteToMove,KingInCheck):
                            pygame.draw.rect(screen,(255,140,140),(100*x,100*y,100,100))
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ChessBoard!=OneMoveBackChessBoard and OneMoveBackChessBoard:
            print ('move undone')
            ChessBoard=OneMoveBackChessBoard
            if WhiteToMove: WhiteToMove=False
            else: WhiteToMove=True
            backgroundreset()
        if event.type == pygame.QUIT:
            pygame.quit()
    #IsKingInCheck(ChessBoard,WhiteToMove)
    UpdatePiecePositions()
    pygame.display.update()
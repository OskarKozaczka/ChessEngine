import pygame
from utility import MoveValidator,IsKingInCheck
import copy
from Chess import ChessBoard

pygame.init()
screen= pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load('./Pieces/bn.png'))


def backgroundreset():
    ChessBoard.BoardColors=[(47, 121, 173),(169, 175, 176)]

    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen,ChessBoard.BoardColors[y%2-x%2],(100*x,100*y,100,100))
backgroundreset()


def UpdatePiecePositions():
    Offset=15
    for y in range(8):
        for x in range(8):
            if ChessBoard.Board[x][y]!='  ': 
                Piece=pygame.image.load('Pieces/{}.png'.format(ChessBoard.Board[x][y]))
                screen.blit(Piece,(100*y+Offset,100*x+Offset))

def RedCheckSquare():
    if IsKingInCheck(ChessBoard.Board,ChessBoard.WhiteToMove):
        PosOfKing=0
        for x in range(8):
            for y in range(8):
                if ChessBoard.Board[y][x]=='wk' and ChessBoard.WhiteToMove: PosOfKing=[x,y]
                if ChessBoard.Board[y][x]=='bk' and ChessBoard.WhiteToMove ==False: PosOfKing=[x,y]
        pygame.draw.rect(screen,(255,0,0),(100*PosOfKing[0],100*PosOfKing[1],100,100))

def DrawLegalMoves():
    for x in range(8):
        for y in range(8):
            if MoveValidator(PieceSelectedPos,[x,y],PieceSelectedType,ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle):
                pygame.draw.rect(screen,(255,140,140),(100*x,100*y,100,100))

PieceSelectedPos=False
OneMoveBackChessBoard=False

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if PieceSelectedPos:
                if MoveValidator(PieceSelectedPos,SquareClicked,PieceSelectedType,ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle):
                    OneMoveBackChessBoard=copy.deepcopy(ChessBoard.Board)
                    move=(PieceSelectedType,PieceSelectedPos,SquareClicked)
                    ChessBoard.Move(move)
                    ChessBoard.debug()
                    ChessBoard.CheckForEndgameConditions()
                backgroundreset()
                RedCheckSquare()
                PieceSelectedPos=False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            if ChessBoard.Board[SquareClicked[1]][SquareClicked[0]]!='  ':
                PieceSelectedPos=SquareClicked
                PieceSelectedType=ChessBoard.Board[PieceSelectedPos[1]][PieceSelectedPos[0]]
                backgroundreset()
                DrawLegalMoves()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and ChessBoard.Board!=OneMoveBackChessBoard and OneMoveBackChessBoard:
            print ('move undone')
            ChessBoard.Board=OneMoveBackChessBoard
            if ChessBoard.WhiteToMove: ChessBoard.WhiteToMove=False
            else: ChessBoard.WhiteToMove=True
            backgroundreset()
        if event.type == pygame.QUIT:
            pygame.quit()
    UpdatePiecePositions()
    pygame.display.update()
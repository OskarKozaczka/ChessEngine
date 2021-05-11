import pygame
from numpy import array
from utility import IsThisStalemate,IsKingInCheck,ListEveryLegalMove
from Engine import EvaluateBestMove,SearchBestMove
from time import sleep
from Chess import ChessBoard

pygame.init()
screen= pygame.display.set_mode((800,800))
pygame.display.set_caption('Chess')
pygame.display.set_icon(pygame.image.load('./Pieces/bn.png'))




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


def EngineMove():
    move=SearchBestMove(2)
    ChessBoard.Move(move)


MoveCount=0
while True:
    pygame.event.pump()
    print("Move",MoveCount)
    MoveCount+=1
    if MoveCount>300:
        ChessBoard.setup()
        MoveCount=0
    if len(ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle))>0:
        EngineMove()
        ChessBoard.debug()
    backgroundreset()
    RedCheckSquare()
    UpdatePiecePositions()
    pygame.display.update()
    if ChessBoard.CheckForEndgameConditions=="Mate":
        sleep(5)
        MoveCount=0
        ChessBoard.setup()
    elif ChessBoard.CheckForEndgameConditions=="Stalemate":
        sleep(5)
        MoveCount=0
        ChessBoard.setup()

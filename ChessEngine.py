import pygame
import numpy as np

pygame.init()

screen= pygame.display.set_mode((800,800))

pygame.display.set_caption('Chess')

white=(255,255,255)
red=(255,0,0)
green=(0,255,0)



Sides=['w','b']

ChessBoard=[["  " for i in range(8)] for i in range (8)]
for x in range(8): 
    ChessBoard[1][x]='bp'
    ChessBoard[6][x]='wp'


Side=['r','n','b','q','k','b','n','r']
for i in range(8):
    ChessBoard[0][i]='b'+Side[i]
    ChessBoard[7][i]='w'+Side[i]
print(np.array(ChessBoard))

def update():

    screen.fill(white)
    ChessBoardColors=[(47, 121, 173),(169, 175, 176)]

    for y in range(8):
        for x in range(8):
            pygame.draw.rect(screen,ChessBoardColors[y%2-x%2],(100*x,100*y,100,100))


    Offset=15
    for y in range(8):
        for x in range(8):
            if ChessBoard[x][y]!='  ': 
                Piece=pygame.image.load('Pieces/{}.png'.format(ChessBoard[x][y]))
                screen.blit(Piece,(100*y+Offset,100*x+Offset))



PieceSelected=False
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            SquareClicked=[pos[0]//100,pos[1]//100]
            print(SquareClicked)
            if PieceSelected:
                print(np.array(ChessBoard))
                ChessBoard[SquareClicked[1]][SquareClicked[0]]=ChessBoard[PieceSelected[1]][PieceSelected[0]]
                ChessBoard[PieceSelected[1]][PieceSelected[0]]='  '
                PieceSelected=False
            else:
                PieceSelected=SquareClicked


        if event.type == pygame.QUIT:
            pygame.quit()
    update()
    pygame.display.update()
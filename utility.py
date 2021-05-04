import copy
import itertools as it
from random import randint
def MoveValidator(startpos,endpos,piece,board,WhiteToMove,Castle):
    
    SeemsLegal=False
    
    if WhiteToMove and piece[0]=='b': return False
    if WhiteToMove==False and piece[0]=='w': return False

    if board[endpos[1]][endpos[0]][0]==board[startpos[1]][startpos[0]][0]: return False
    
    if piece=='wp':
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0] and board[startpos[1]-1][startpos[0]]=="  ": SeemsLegal=True
        if endpos[1]==startpos[1]-2 and startpos[1]==6 and endpos[0]==startpos[0]  and board[startpos[1]-2][startpos[0]]=="  " and board[startpos[1]-1][startpos[0]]=="  " : SeemsLegal=True 
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]-1 and board[endpos[1]][endpos[0]][0]=='b': SeemsLegal=True
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]+1 and board[endpos[1]][endpos[0]][0]=='b': SeemsLegal=True
            
    if piece=='bp':
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0] and board[startpos[1]+1][startpos[0]]=="  ": SeemsLegal=True    
        if endpos[1]==startpos[1]+2 and startpos[1]==1 and endpos[0]==startpos[0] and board[startpos[1]+2][startpos[0]]=="  " and board[startpos[1]+1][startpos[0]]=="  ": SeemsLegal=True    
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0]-1 and board[endpos[1]][endpos[0]][0]=='w': SeemsLegal=True 
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0]+1 and board[endpos[1]][endpos[0]][0]=='w': SeemsLegal=True

    if piece=='wb' or piece=='bb' or piece=='wq' or piece=='bq':
        if endpos[0]-startpos[0]==endpos[1]-startpos[1] or endpos[0]+endpos[1]==startpos[0]+startpos[1]:

            for i in range(1,min(startpos[1],7-startpos[0])+1):
                if endpos==[startpos[0]+i,startpos[1]-i]: SeemsLegal=True
                if board[startpos[1]-i][startpos[0]+i]!='  ':break

            for i in range(1,min(startpos[0],7-startpos[1])+1):
                if endpos==[startpos[0]-i,startpos[1]+i]: SeemsLegal=True
                if board[startpos[1]+i][startpos[0]-i]!='  ':break

            for i in range(1,min(7-startpos[1],7-startpos[0])+1):
                if endpos==[startpos[0]+i,startpos[1]+i]: SeemsLegal=True
                if board[startpos[1]+i][startpos[0]+i]!='  ':break

            for i in range(1,min(startpos[0],startpos[1])+1):
                if endpos==[startpos[0]-i,startpos[1]-i]: SeemsLegal=True
                if board[startpos[1]-i][startpos[0]-i]!='  ':break

            
    if piece=='wr' or piece=='br' or piece=='wq' or piece=='bq':
        if endpos[0]==startpos[0] or endpos[1]==startpos[1]:
        
            for i in range(1,7-startpos[1]+1):
                if endpos[1]==startpos[1]+i: SeemsLegal=True
                if board[startpos[1]+i][startpos[0]]!='  ':break

            for i in range(1,startpos[1]+1):
                if endpos[1]==startpos[1]-i: SeemsLegal=True
                if board[startpos[1]-i][startpos[0]]!='  ':break

            for i in range(1,7-startpos[0]+1):
                if endpos[0]==startpos[0]+i: SeemsLegal=True
                if board[startpos[1]][startpos[0]+i]!='  ':break

            for i in range(1,startpos[0]+1):
                if endpos[0]==startpos[0]-i: SeemsLegal=True
                if board[startpos[1]][startpos[0]-i]!='  ':break

    if piece=='wn' or piece=='bn':
        possibilities=list(it.permutations([-2,-1,2,1],2))
        for i in possibilities:
            if abs(i[0])-abs(i[1])!=0 and endpos==[startpos[0]+i[0],startpos[1]+i[1]]:
                SeemsLegal=True

    if piece=='wk' or piece=='bk':
        if endpos==startpos: return False  
        if startpos[1]-1<=endpos[1]<=startpos[1]+1 and startpos[0]-1<=endpos[0]<=startpos[0]+1: SeemsLegal=True
        
        if startpos[0]+2==endpos[0] and startpos[1]==endpos[1]:
            if board[startpos[1]][startpos[0]+1]=="  " and board[startpos[1]][startpos[0]+2]=="  ":
                if IsKingInCheck(board,WhiteToMove)==False: 
                    if "K" in Castle if WhiteToMove else "k" in Castle: SeemsLegal=True
        if startpos[0]-2==endpos[0] and startpos[1]==endpos[1]:
            if board[startpos[1]][startpos[0]-1]=="  " and board[startpos[1]][startpos[0]-2]=="  "and board[startpos[1]][startpos[0]-3]=="  ":
                if IsKingInCheck(board,WhiteToMove)==False: 
                    if "Q" in Castle if WhiteToMove else "q" in Castle: SeemsLegal=True



    if SeemsLegal:
        board2=copy.deepcopy(board)
        board2[endpos[1]][endpos[0]]=piece
        board2[startpos[1]][startpos[0]]='  '
        if IsKingInCheck(board2,WhiteToMove)==False: return True
    return False

def IsKingInCheck(board,WhiteToMove):
    PosOfKing=0
    for x in range(8):
        for y in range(8):
            if board[y][x]=='wk' and WhiteToMove: 
                PosOfKing=[x,y]
                break
            if board[y][x]=='bk' and WhiteToMove == False: 
                PosOfKing=[x,y]
                break
    if PosOfKing==0: return True
    for x in range(8):
        for y in range(8):
            if MoveValidator([x,y],PosOfKing,board[y][x],board,False if WhiteToMove else True,""):
                return True
    return False
            

def ToPositionInFENNotation(board,WhiteToMove,Castle):
    string=''
    for row in board:
        string+='/'
        Blanks=0
        for square in row:
            if square!='  ':
                if Blanks!=0:
                    string+=str(Blanks)
                    Blanks=0
                string+=square[1] if square[0]=='b' else square[1].upper() 
            else:
                Blanks+=1
        if Blanks!=0 and square==row[-1]: string+=str(Blanks)



    string= string[1:]+(" w " if WhiteToMove else " b ")
    string+=Castle
    return string+" - 0 1"

def ToStatndardNotation(Move):
    Letters=['a','b','c','d','e','f','g','h']
    string=''
    if Move[0][1]!='p': string+=Move[0][1]
    string+=Letters[Move[2][0]]
    string+=str(7-Move[2][1])
    return string

def ListEveryLegalMove(ChessBoard,WhiteToMove,Castle):
    ListOfMoves=[]
    for xx in range(8):
        for yy in range(8):
            for x in range(8):
                for y in range(8):
                    if MoveValidator([xx,yy],[x,y],ChessBoard[yy][xx],ChessBoard,WhiteToMove,Castle):
                        ListOfMoves.append((ChessBoard[yy][xx],[xx,yy],[x,y]))
    return ListOfMoves

def IsThisStalemate(ChessBoard,WhiteToMove):
    if len(ListEveryLegalMove(ChessBoard,WhiteToMove,''))==0: return True
    PieceCounter=0
    for y in range(8):
        for x in range(8):
            if ChessBoard[y][x]!='  ' and ChessBoard[y][x][1]!='n' and ChessBoard[y][x][1]!='b': PieceCounter+=1
    if PieceCounter==2: return True
    return False

def RandomMove(Moves):
    return Moves[randint(0,len(Moves)-1)]


def FormatMove(Move,board):
    #from ('bb', 3, 2)
    #to ['bb',(x,y),(3,2)]
    moves=[]
    for x in range(8):
        for y in range(8):
            if board[y][x]==Move[0]:
                moves.append([Move[0],(y,x),(Move[1],7-Move[2])])

    return moves
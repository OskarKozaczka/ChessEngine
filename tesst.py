import copy
import itertools as it
from numpy import array
def MoveValidator(startpos,endpos,piece,board,WhiteToMove):
    
    SeemsLegal=False
    
    if WhiteToMove and piece[0]=='b': return False
    if WhiteToMove==False and piece[0]=='w': return False

    if board[endpos[1]][endpos[0]][0]==board[startpos[1]][startpos[0]][0]: return False
    
    if piece=='wp':
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0] and board[startpos[1]-1][startpos[0]]=="  ": SeemsLegal=True
        if endpos[1]==startpos[1]-2 and startpos[1]==6 and endpos[0]==startpos[0]  and board[startpos[1]-2][startpos[0]]=="  ": SeemsLegal=True 
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]-1 and board[endpos[1]][endpos[0]][0]=='b': SeemsLegal=True
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]+1 and board[endpos[1]][endpos[0]][0]=='b': SeemsLegal=True
            
    if piece=='bp':
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0] and board[startpos[1]+1][startpos[0]]=="  ": SeemsLegal=True    
        if endpos[1]==startpos[1]+2 and startpos[1]==1 and endpos[0]==startpos[0] and board[startpos[1]+2][startpos[0]]=="  ": SeemsLegal=True    
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



    if SeemsLegal:
        board2=copy.deepcopy(board)
        board2[endpos[1]][endpos[0]]=piece
        board2[startpos[1]][startpos[0]]='  '
        if IsKingInCheck(board2,False if WhiteToMove else True)==False: return True
    return False

def IsKingInCheck(board,WhiteToMove):
    PosOfKing=0
    
    for x in range(8):
        for y in range(8):
            if board[y][x]=='wk' and WhiteToMove: 
                PosOfKing=[x,y]
                break
            if board[y][x]=='bk' and WhiteToMove ==False: 
                PosOfKing=[x,y]
                break
    if PosOfKing==0: return False
    for x in range(8):
        for y in range(8):
            if MoveValidator([x,y],PosOfKing,board[y][x],board,False if WhiteToMove else True):
                return True
    return False
            


board=[['br', 'bn', 'bb', '  ', 'bk', 'bb', 'bn', 'br'],
 ['bp', 'bp', 'bp', '  ', '  ', '  ', 'bp', 'bp'],
['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
['  ', 'wb', '  ', 'bp', 'bp', 'bp', '  ', '  '], 
['  ', '  ', '  ', 'wp', 'wp', 'wp', '  ', 'bq'], 
['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '], 
['wp', 'wp', 'wp', '  ', '  ', '  ', 'wp', 'wp'], 
['wr', 'wn', 'wb', 'wq', 'wk', '  ', 'wn', 'wr']]

print(MoveValidator([1,3],[4,0],'wb',board,True))
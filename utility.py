import itertools as it
def MoveValidator(startpos,endpos,piece,board,WhiteToMove):
    
    if WhiteToMove and piece[0]=='b': return False
    if WhiteToMove==False and piece[0]=='w': return False


    if board[endpos[1]][endpos[0]][0]==board[startpos[1]][startpos[0]][0]:
        return False

    if piece=='wp':
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0] and board[startpos[1]-1][startpos[0]]=="  ": return True
        if endpos[1]==startpos[1]-2 and startpos[1]==6 and endpos[0]==startpos[0]  and board[startpos[1]-2][startpos[0]]=="  ": return True 
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]-1 and board[endpos[1]][endpos[0]][0]=='b': return True
        if endpos[1]==startpos[1]-1 and endpos[0]==startpos[0]+1 and board[endpos[1]][endpos[0]][0]=='b': return True
            
    if piece=='bp':
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0] and board[startpos[1]+1][startpos[0]]=="  ": return True    
        if endpos[1]==startpos[1]+2 and startpos[1]==1 and endpos[0]==startpos[0] and board[startpos[1]+2][startpos[0]]=="  ": return True    
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0]-1 and board[endpos[1]][endpos[0]][0]=='w': return True 
        if endpos[1]==startpos[1]+1 and endpos[0]==startpos[0]+1 and board[endpos[1]][endpos[0]][0]=='w': return True

    if piece=='wb' or piece=='bb' or piece=='wq' or piece=='bq':
        
        for i in range(1,min(7-startpos[0],7-startpos[1])):
            if endpos==[startpos[0]+i,startpos[1]+i]: return True 
            if board[startpos[1]+i][startpos[0]+i]!='  ': break
        for i in range(1,min(7-startpos[0],7-startpos[1])):
            if endpos==[startpos[0]-i,startpos[1]-i]: return True 
            if board[startpos[1]-i][startpos[0]-i]!='  ': break
        for i in range(1,min(7-startpos[0],7-startpos[1])):
            if endpos==[startpos[0]-i,startpos[1]+i]: return True 
            if board[startpos[1]+i][startpos[0]-i]!='  ': break
        for i in range(1,min(7-startpos[0],7-startpos[1])):
            if endpos==[startpos[1]+i,startpos[0]-i]: return True 
            if board[startpos[0]-i][startpos[1]+i]!='  ': break
            
    if piece=='wr' or piece=='br' or piece=='wq' or piece=='bq':
        if endpos[0]==startpos[0] or endpos[1]==startpos[1]:
            return True

    if piece=='wn' or piece=='bn':
        possibilities=list(it.permutations([-2,-1,2,1],2))
        for i in possibilities:
            if abs(i[0])-abs(i[1])!=0 and endpos==[startpos[0]+i[0],startpos[1]+i[1]]:
                return True

    if piece=='wk':
        if endpos==startpos: return False  
        if startpos[1]-1<endpos[1]<startpos[1]+1 and startpos[0]-1<endpos[1]<startpos[0]+1: return True

    return False

from numpy import array
from utility import IsKingInCheck,ToPositionInFENNotation,IsThisStalemate,ListEveryLegalMove


def setup():
    Board=[["  " for i in range(8)] for i in range (8)]
    for x in range(8): 
        Board[1][x]='bp'
        Board[6][x]='wp'
    
    Side=['r','n','b','q','k','b','n','r']
    for i in range(8):
        Board[0][i]='b'+Side[i]
        Board[7][i]='w'+Side[i]
    return Board


class ChessBoard:

    Board=setup()
    Castle = "KQkq"
    WhiteToMove = True

    @staticmethod
    def setup():
        Board=[["  " for i in range(8)] for i in range (8)]
        for x in range(8): 
            Board[1][x]='bp'
            Board[6][x]='wp'
        
        Side=['r','n','b','q','k','b','n','r']
        for i in range(8):
            Board[0][i]='b'+Side[i]
            Board[7][i]='w'+Side[i]
        ChessBoard.Board=Board
        ChessBoard.Castle = "KQkq"
        ChessBoard.WhiteToMove = True

    @staticmethod
    def Move(move):
        Board=ChessBoard.Board
        WhiteToMove=ChessBoard.WhiteToMove
        Board[move[2][1]][move[2][0]]=move[0]
        Board[move[1][1]][move[1][0]]="  "

        if WhiteToMove:
            for square in Board[0]:
                if square =="wp": Board[0][Board[0].index(square)]='wq'
        else:
            for square in Board[7]:
                if square=="bp": Board[7][Board[7].index(square)]='bq'

        if move[0][1]=='k' and move[1][0]-move[2][0]==-2:
            Board[move[1][1]][move[1][0]+3]='  '
            Board[move[1][1]][move[1][0]+1]='wr' if WhiteToMove else 'br'
        if move[0][1]=='k' and move[1][0]-move[2][0]==2:
            Board[move[1][1]][move[1][0]-4]='  '
            Board[move[1][1]][move[1][0]-1]='wr' if WhiteToMove else 'br'

        if Board[7][7]!="wr": ChessBoard.Castle=ChessBoard.Castle.replace("K",'')
        if Board[7][0]!="wr": ChessBoard.Castle=ChessBoard.Castle.replace("Q",'')
        if Board[0][7]!="br": ChessBoard.Castle=ChessBoard.Castle.replace("k",'')
        if Board[0][0]!="br": ChessBoard.Castle=ChessBoard.Castle.replace("q",'')
        if Board[7][4]!="wk": 
            ChessBoard.Castle=ChessBoard.Castle.replace("K",'')
            ChessBoard.Castle=ChessBoard.Castle.replace("Q",'')
        if Board[0][4]!="bk":
            ChessBoard.Castle=ChessBoard.Castle.replace("k",'')
            ChessBoard.Castle=ChessBoard.Castle.replace("q",'')
        ChessBoard.WhiteToMove=False if ChessBoard.WhiteToMove else True

    @staticmethod
    def debug():
        print(array(ChessBoard.Board),'\n')
        print("Check",IsKingInCheck(ChessBoard.Board,ChessBoard.WhiteToMove))
        print(ToPositionInFENNotation(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle))
        print(ChessBoard.Castle)

    @staticmethod
    def CheckForEndgameConditions():
        if len(ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle))==0 and IsKingInCheck(ChessBoard.Board,ChessBoard.WhiteToMove):
            print("That is Mate")
            return "Mate"
        elif IsThisStalemate(ChessBoard.Board,ChessBoard.WhiteToMove):
            print("That is Stalemate")
            return "Stalemate"
        

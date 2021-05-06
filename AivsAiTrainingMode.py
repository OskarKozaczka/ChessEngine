from utility import IsThisStalemate,IsKingInCheck,ListEveryLegalMove
from Engine import EvaluateBestMove,SearchBestMove
from Chess import ChessBoard


MoveCount=0


def EngineMove():
    move=SearchBestMove(2)
    ChessBoard.Move(move)
  
    
while True:
    print("Move",MoveCount)
    MoveCount+=1
    if MoveCount>300:
        ChessBoard.setup()
        MoveCount=0
    if len(ListEveryLegalMove(ChessBoard.Board,ChessBoard.WhiteToMove,ChessBoard.Castle))>0:
        EngineMove()
        ChessBoard.debug()
    if ChessBoard.CheckForEndgameConditions=="Mate":
        MoveCount=0
        ChessBoard.setup()
    elif ChessBoard.CheckForEndgameConditions=="Stalemate":
        MoveCount=0
        ChessBoard.setup()


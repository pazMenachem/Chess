from abc import ABC
from Piece import Piece

class Pawn(Piece, ABC):
    def __init__(self,path,width,height,color,pieceChar):
        super().__init__(path,width,height,color,pieceChar)
        self._moved = False
    # def move(self):



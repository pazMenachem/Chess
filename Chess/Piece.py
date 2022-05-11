from abc import abstractmethod

import pygame

class Piece:
    def __init__(self):
        pass
    def __init__(self,path,width,height,color,pieceChar):
        self._piece = pygame.image.load(path).convert_alpha()
        self._pieceChar = pieceChar
        self._pieceLoc = self._piece.get_rect()
        self._color = color
        self._inGame = True
        pygame.transform.smoothscale(self._piece,(width,height))

    def getColor(self):
        return self._color

    def getPieceChar(self):
        return self._pieceChar

    def getLoc(self):
        return self._pieceLoc

    def setLoc(self,newX = None,newY = None):
        self._pieceLoc[0] = newX
        self._pieceLoc[1] = newY

    def getPiece(self):
        return self._piece

    @abstractmethod
    def move(self):
        pass

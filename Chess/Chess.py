import pygame
from pygame.locals import *
from Board import Board

class Chess:
    def __init__(self,width = 800,height = 800):
        self._board = Board(width,height)
        self._onGoing = True

    def _draw(self):
        self._board.draw()

    def _move(self):
        x,y = pygame.mouse.get_pos()
        position = self._getPos(x,y)
        if self._board.getHang():
            self._board.validMove(position)
        else:
            self._board.hangPiece(position)

    def _getPos(self,x,y):
        return (y//100) * 8 + x//100

    def start(self):
        pygame.init()

        while self._onGoing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self._onGoing = False
                if event.type == MOUSEBUTTONDOWN:
                    self._move()

            self._draw()
            pygame.display.update()
        pygame.quit()

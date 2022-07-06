import pygame
from enum import Enum

# ['br', 'bh', 'bb', 'bk', 'bq', 'bb', 'bh', 'br',
#  'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp',
#  '0', '0', '0', '0', '0', '0', '0', '0',
#  '0', '0', '0', '0', '0', '0', '0', '0',
#  '0', '0', '0', '0', '0', '0', '0', '0',
#  '0', '0', '0', '0', '0', '0', '0', '0',
#  'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp',
#  'wr', 'wh', 'wb', 'wk', 'wq', 'wb', 'wh', 'wr', '0']

class PieceE(Enum):
    bPawn = 'bp'
    bHorse = 'bh'
    bBishop = 'bb'
    bRook = 'br'
    bQueen = 'bq'
    bKing = 'bk'

    wPawn = 'wp'
    wHorse = 'wh'
    wBishop = 'wb'
    wRook = 'wr'
    wQueen = 'wq'
    wKing = 'wk'

class Board:
    # ---------------------
    # Main Functions
    # ---------------------
    def __init__(self, width, height):
        """
        # Constructor for the Board class.
        @:parameter
        # width - The Width of the Board.
        # height - The height of the Board.
        # board - The Window of the Board.
        # pieces - String array of the pieces.
        # hang - Boolean indicator whether a piece is BEING moved.
        # hangedPieceLoc - Last location of the hanged piece.
        # options - Set of illegal move options for the hanged piece.
        """
        self._width = width
        self._height = height
        self._board = pygame.display.set_mode((width, height))
        self._pieces = ['0', '0', '0', '0', 'wh', '0', '0', '0',
                        '0', 'bk', '0', '0', '0', 'wr', 'bp', '0',
                        '0', '0', '0', 'wq', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0', '0', '0', '0',
                        '0', '0', '0', 'bk', '0', '0', '0', '0',
                        '0', '0', '0', '0', '0', '0', '0', '0',
                        '0', 'bb', 'wp', '0', '0', '0', 'wr', '0',
                        '0', '0', '0', '0', '0', '0', '0', '0', '0']

        self._hang = False
        self._hangedPieceLoc = None
        self._options = None
        pygame.display.set_caption("Awesome Chess")

    def draw(self):
        """
        # Main function which draws the Board.
        """
        self._board.fill((92, 69, 47))
        odd = 0
        position = 0
        ## Draws the Board
        for row in range(8):
            odd = (odd + 1) % 2
            for col in range(4):
                pygame.draw.rect(self._board,
                                 (225, 203, 182),
                                 (odd * (self._height // 8) + col * self._height // 4,
                                  row * (self._height // 8),
                                  self._width // 8, self._height // 8))

        ## highLight options of piece
        if self._options:
            for i in self._options:
                s = pygame.Surface((self._width // 8, self._height // 8))
                s.set_alpha(128)
                s.fill((181, 245, 78))
                self._board.blit(s, (100 * (i % 8), 100 * (i // 8)))

        ## Draws the Pieces.
        for i in self._pieces:
            if i == '/':  ## <- Why did i wrote that...?
                continue

            if i == '0':
                position += 1
                continue

            self._board.blit(pygame.image.load("data//" + self._pieces[position] + ".png"),
                             ((position % 8) * 100, (position // 8) * 100))
            position += 1

            ## Draws the hanged Piece next to mouse
            if self._hang:
                self._board.blit(pygame.image.load("data//" + self._pieces[64] + ".png"),
                                 (pygame.mouse.get_pos()[0] - 50,
                                  pygame.mouse.get_pos()[1] - 50))

    def validMove(self, position):
        """
        # With given position, the function checks
        # whether the move is valid by going through
        # the Piece legal moves.
        """
        if position in self._legalMoves(self._pieces[64][1]):
            self._makeMove(position)
            # self.checkStat()
        else:
            print("invalid move")

    def _legalMoves(self, piece):
        """
        #   Main function which makes
        #   a set of moves for each piece.
        #   First it calculates all the options,
        #   later on deletes the illegal ones.
        #   which allow the pawn to "eat".
        #   The function returns the legal moves for certain piece.
        """
        moves = set()
        match piece:

            case 'p':
                moves = self._pawnMovesOption()
                moves.update(self._pawnEatOption())

            case 'k':
                moves = self._kingMovesOptions()
                # If hang is True - means that we need to check
                # spots which might threats the king piece.
                # if self._hang:

            case 'r':
                moves = self._getLinesRowsCords()
                moves.difference_update(self._cantEatOptions(moves))

            case 'b':
                moves = self._getDiagonalCords()
                moves.difference_update(self._cantEatOptions(moves))

            case 'q':
                moves.update(self._getDiagonalCords())
                moves.update(self._getLinesRowsCords())
                moves.difference_update(self._cantEatOptions(moves))

            case 'h':
                moves.update(self._knightOptions())
                moves.difference_update(self._knightOptionsCheck(moves))
                moves.difference_update(self._cantEatOptions(moves))

        moves.add(self._hangedPieceLoc)
        return moves

    def hangPiece(self, position):
        """
        # With given position the Function
        # places the piece in the "hanged" spot(64).
        # clears the piece location.
        # marks that a piece is "hanged".
        # saves the location of the piece (hanged Piece Loc).
        # gets a set of all the legal moves for the certain Piece.
        """
        ## if none piece was selected
        if self._pieces[position] == '0':
            return

        self._pieces[64] = self._pieces[position]
        self._pieces[position] = '0'
        self._hang = True
        self._hangedPieceLoc = position
        self._options = self._legalMoves(self._pieces[64][1])

    def _makeMove(self,newPosition):
        """
        # - After Verifying - the new location for the hanged piece,
        # the function sets the piece at its new location.
        # also resets the fields hanged, spot 64 and options.
        """
        self._pieces[newPosition] = self._pieces[64]
        self._hang = False
        self._pieces[64] = '0'
        self._options = None
        # self._hangedPieceLoc = newPosition

    def _oppositeTeamAllOptions(self):
        """
        # The function returns all the legal moves
        # that the opposite team can do.
        # use for "Check".
        """

        oppositeColor = ''

    # ---------------------
    # Getters and Setters
    # ---------------------

    def _freeSpot(self,position):
        """
        # Checks whether the given position
        # is taken or not.
        """
        return self._pieces[position] == '0'

    def getWidth(self):
        """
        # Returns the width of the Board.
        """
        return self._width

    def getHeight(self):
        """
        # Returns the height of the Board.
        """
        return self._height

    def getHang(self):
        """
        # Returns the piece which is "hanged".
        # - in spot pieces[64]
        """
        return self._hang

    # ---------------------
    # Pieces Move Options
    # ---------------------
    def _knightOptionsCheck(self,moves):
        """
        #   Returns the set of moves
        #   which illegal for the knight piece.
        """
        illegalMoves = set()
        for i in moves:
            if i < 0 or i > 63:
                illegalMoves.add(i)
            if abs( (self._hangedPieceLoc % 8) - ( i % 8) ) > 2:
                illegalMoves.add(i)
        return illegalMoves

    def _cantEatOptions(self,moves):
        """
        #   Returns the set of moves
        #   which illegal for the hanged piece.
        """
        illegalMoves = set()
        ## black Piece
        if self._pieces[64][0] == 'b':
            for i in moves:
                if self._pieces[i][0] == 'b':
                    illegalMoves.add(i)

        ## white Piece
        if self._pieces[64][0] == 'w':
            for i in moves:
                if self._pieces[i][0] == 'w':
                    illegalMoves.add(i)
        return illegalMoves

    def _pawnEatOption(self):
        """
        #   Returns the set of moves
        #   which allow the pawn to "eat".
        """
        moves = set()
        if self._pieces[64][0] == 'b':  ## Black Pawn
            ## when pawn eats Down - Right
            if self._pieces[self._hangedPieceLoc + 9][0] == 'w' and (self._hangedPieceLoc + 9) % 8 != 0:
                moves.add(self._hangedPieceLoc + 9)

            ## when pawn eats Down - Left
            if self._pieces[self._hangedPieceLoc + 7][0] == 'w' and self._hangedPieceLoc % 8 != 0:
                moves.add(self._hangedPieceLoc + 7)
        else:
            ## when pawn eats Up - Left
            if self._pieces[self._hangedPieceLoc - 9][0] == 'b' and self._hangedPieceLoc % 8 != 0:
                moves.add(self._hangedPieceLoc - 9)

            ## when pawn eats Down - Right
            if self._pieces[self._hangedPieceLoc - 7][0] == 'b' and (self._hangedPieceLoc - 7) % 8 != 0:
                moves.add(self._hangedPieceLoc - 7)
        return moves

    def _getLinesRowsCords(self):
        """
        #   Returns the set of moves
        #   for row spots.
        #   used for queen and rook pieces.
        """
        cordSet = set()

        # row checking left side of piece
        cord = self._hangedPieceLoc - 1
        while cord != (( self._hangedPieceLoc // 8 ) * 8) - 1:
            if not self._freeSpot(cord):
                cordSet.add(cord)
                break
            cordSet.add(cord)
            cord -= 1

        # row checking right side of piece
        cord = self._hangedPieceLoc + 1
        while cord != ((self._hangedPieceLoc // 8) * 8) + 8:
            if not self._freeSpot(cord):
                cordSet.add(cord)
                break
            cordSet.add(cord)
            cord += 1

        # col checking upper side
        cord = self._hangedPieceLoc - 8
        while cord >= 0:
            if not self._freeSpot(cord):
                cordSet.add(cord)
                break
            cordSet.add(cord)
            cord -= 8

        # col checking downside
        cord = self._hangedPieceLoc + 8
        while cord < 64:
            if not self._freeSpot(cord):
                cordSet.add(cord)
                break
            cordSet.add(cord)
            cord += 8

        return cordSet

    def _getDiagonalCords(self):
        """
        #   Returns the set of moves
        #   for diagonal spots.
        #   used for queen and bishop pieces.
        """
        cordSet = set()

        if self._hangedPieceLoc % 8 != 0:

            # left upper side of piece
            cord = self._hangedPieceLoc - 9
            while cord >= 0:
                if not self._freeSpot(cord) or cord % 8 == 0:
                    cordSet.add(cord)
                    break
                cordSet.add(cord)
                cord -= 9

            #  Down Left side
            cord = self._hangedPieceLoc + 7
            while cord < 64:
                if not self._freeSpot(cord) or cord % 8 == 0:
                    cordSet.add(cord)
                    break
                cordSet.add(cord)
                cord += 7

        if self._hangedPieceLoc % 8 != 7:

            # right upper side of piece
            cord = self._hangedPieceLoc - 7
            while cord >= 1:
                if cord % 8 == 7 or not self._freeSpot(cord):
                    cordSet.add(cord)
                    break
                cordSet.add(cord)
                cord -= 7

            # Down Right side
            cord = self._hangedPieceLoc + 9
            while cord < 64:
                if not self._freeSpot(cord) or cord % 8 == 7:
                    cordSet.add(cord)
                    break
                cordSet.add(cord)
                cord += 9

        return cordSet

    def _kingMovesOptions(self):
        moves = {self._hangedPieceLoc - 9,self._hangedPieceLoc - 8,self._hangedPieceLoc - 7,
                             self._hangedPieceLoc - 1, self._hangedPieceLoc + 1,
                             self._hangedPieceLoc + 9,self._hangedPieceLoc + 8,self._hangedPieceLoc + 7}
        legalMoves = set()
        for i in moves:
            ## if piece is on left boarder
            if self._hangedPieceLoc % 8 == 0:
                if i % 8 == 7:
                    continue
            ## if piece is on right boarder
            if self._hangedPieceLoc % 8 == 7:
                if i % 8 == 0:
                    continue
            if self._freeSpot(i % 64):
                legalMoves.add(i % 64)
            if self._pieces[64][0] == 'w':  ## if white king
                if self._pieces[i % 64][0] == 'b':
                    legalMoves.add(i % 64)
            if self._pieces[64][0] == 'b':  ## if black king
                if self._pieces[i % 64][0] == 'w':
                    legalMoves.add(i % 64)
        return moves.intersection(legalMoves)

    def _knightOptions(self):
        return {self._hangedPieceLoc - 10, self._hangedPieceLoc - 17,
                              self._hangedPieceLoc - 15, self._hangedPieceLoc - 6,
                              self._hangedPieceLoc + 10, self._hangedPieceLoc + 17,
                              self._hangedPieceLoc + 15, self._hangedPieceLoc + 6}

    def _pawnMovesOption(self):
        moves = set()
        if self._pieces[64][0] == 'b':  ## Black Pawn

            ## when pawn didn't make a move before
            if 7 < self._hangedPieceLoc < 16 and self._freeSpot(self._hangedPieceLoc + 16):
                moves.add(self._hangedPieceLoc + 16)

            ## when pawn moves normally
            if self._freeSpot(self._hangedPieceLoc + 8):
                moves.add(self._hangedPieceLoc + 8)

        else:
            ## when pawn didn't make a move before
            if 47 < self._hangedPieceLoc < 56 and self._freeSpot(self._hangedPieceLoc - 16):
                moves.add(self._hangedPieceLoc - 16)

            ## when pawn moves normally
            if self._freeSpot(self._hangedPieceLoc - 8):
                moves.add(self._hangedPieceLoc - 8)

        return moves

    # def _getAllOptions(self,color):
    #     options = set()
    #     for i in self._pieces:
    #         if i == '0':
    #             continue
    #         if i[0] == color:
    #             if i[1] == 'p':
    #                 options.update(self._pawnEatOption())
    #                 continue
    #             options.update(self._legalMoves('r'))
    #     return options

    # def checkStat(self):
    #     if self._pieces.index('bk') in self._getAllOptions('w'):
    #         print("check")

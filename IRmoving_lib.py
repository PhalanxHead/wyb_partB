"""****************************************************************************
* irrationalPlayer/moving_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: - Need an update for board when piece dies
*****************************************************************************"""
import IRplayer
import IRplacing_lib
import random

ROW = 0
COL = 1

class Board_State:
    """
    Class that is going to help build our tree for minimax and alpha-beta pruning,
    the class shows all pieces of information relating to that state
    """
    def __init__(self, board, colour, old_pos, new_pos):

        self.board = board
        self.score = None
        self.colour = colour
        self.opponent_pieces = None
        self.piece_locations = None
        self.old_pos = old_pos
        self.new_pos = new_pos

""" ************************************************************************* """

def moving_phase(self, turns):
    """
    Make a random legal move
    Returns:
        move: A token move in the form ((fromCol, fromRow),(toCol, toRow))
    ==============================
    Input Variables:
        self:   A Player object as defined by the specification
        turns:  The number of turns taken (incremented by 1 for each move,
                ie the second round of moves is turns 3 and 4)
    """

    fromSquare = self.piece_locations[random.randrange(0, len(self.piece_locations))]
    legalMoves = getAvailableMoves(self, fromSquare, turns)

    while len(legalMoves) == 0:
        fromSquare = self.piece_locations[random.randrange(0, len(self.piece_locations))]
        legalMoves = getAvailableMoves(self, fromSquare, turns)

    toSquare = legalMoves[random.randrange(0, len(legalMoves))]

    return (fromSquare, toSquare)

""" ************************************************************************* """

def moveCalc(fromSquare, direction):
    """
    Moves the piece in the specified direction
    Returns:
        newSquare:  (row, col)
    ==========================
    Input Variables:
        fromSquare: The square the piece being moved is on, in form (col, row)
        direction:  The direction to move the piece in, in form (0,1) (For Down)
    """
    newSquare_row = fromSquare[ROW] + direction[ROW]
    newSquare_col = fromSquare[COL] + direction[COL]

    return (newSquare_row, newSquare_col)

""" ************************************************************************* """

def getAvailableMoves(self, square, turns):
    """
    Returns a list of the available moves for the square
    """
    legalMoves = []
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]

    for move in buffers:
        newMove = moveCalc(square, move)
        if IRplayer.check_legal(self, newMove, turns) == True:
            legalMoves.append(newMove)

    return legalMoves

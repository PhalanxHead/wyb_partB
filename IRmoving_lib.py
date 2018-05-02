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

    buffers = [(1,0),(-1,0),(0,1),(0,-1)]
    fromSquare = self.piece_locations[random.randrange(0, len(self.piece_locations))]

    bufferInd = random.randrange(0, len(buffers))
    toSquare = moveCalc(fromSquare, buffers[bufferInd])

    while not IRplayer.check_legal(self, toSquare, turns):
        bufferInd = random.randrange(0, len(buffers))
        toSquare = moveCalc(fromSquare, buffers[bufferInd])

    return (fromSquare, toSquare)

""" ************************************************************************* """

def moveCalc(fromSquare, direction):
    """
    Moves the piece in the specified direction
    Returns:
        newSquare:  (row, col)
    ==========================
    Input Variables:
        fromSquare: The square the piece being moved is on, in form (row, col)
        direction:  The direction to move the piece in, in form (0,1) (For Right)
    """
    newSquare_row = fromSquare[ROW] + direction[ROW]
    newSquare_col = fromSquare[COL] + direction[COL]

    return (newSquare_row, newSquare_col)

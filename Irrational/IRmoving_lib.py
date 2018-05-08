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
import player as pl
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
    legal_moves = getAvailableMoves(self, fromSquare, turns)

    while len(legal_moves) == 0:
        fromSquare = self.piece_locations[random.randrange(0, len(self.piece_locations))]
        legal_moves = getAvailableMoves(self, fromSquare, turns)

    toSquare = legal_moves[random.randrange(0, len(legal_moves))]

    return (fromSquare, toSquare)

""" ************************************************************************* """

def getAvailableMoves(player, square, turns):
    """
    Returns:
        A list of the available moves for the square.
    ================================
    Input Variables:
        player: The player class
        square: The piece to check all the moves for
        turns:  The number of turns that have passed
    """
    legal_moves = []
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    for d_row, d_col in dirs:
        new_row = square[ROW] + d_row
        new_col = square[COL] + d_col

        new_move = (new_row, new_col)

        if pl.check_legal(player, new_move, turns):
            legal_moves.append(new_move)

    return legal_moves

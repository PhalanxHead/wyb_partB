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


def moving_phase(self, turns):
    """
    Make a random legal move
    """
    move_set = get_available_moves(self.board, self.piece_locations, turns)

    move = move_set(random.randint(len(move_set)))

    return move

def get_available_moves(board, piece_locations, turns):
    """
    Function that produces all available moves for the player. The structure of
    the output is a list of nested tuples such that we have (old, new) positions.
    """
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]
    all_moves = []

    for old_pos in self.piece_locations:

        for move in buffers:

            new_pos = (old_pos[ROW] + move[ROW], old_pos[COL] + move[COL])

            if check_legal(self.board, new_pos, turns):
                all_moves.append((old_pos, new_pos))

    return all_moves

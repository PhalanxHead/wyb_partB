"""****************************************************************************
* moving_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: - Need an update for board when piece dies
*****************************************************************************"""
from player import *
from placing_lib import *

ROW = 0
COL = 1

class Board_State(board, colour, old_pos, new_pos):
  """
  Class that is going to help build our tree for minimax and alpha-beta pruning,
  the class shows all pieces of information relating to that state
  """
  def __init__(self):

    self.board = board
    self.score = None
    self.colour = colour
    self.opponent_pieces = None
    self.piece_locations = None
    self.old_pos = old_pos
    self.new_pos = new_pos


""" For moving
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):

    move_set = minimax(self, turns)

    return move_set

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

def evaluation_function(state, move):
    """
    Our Evaluation function that determines a score for a specific game state,
    this score is then used within the minimax algorithm to find the optimal play
    """
    score = 0
    dead = False

    if check_self_die(state, move):
        score = 5
        dead = True

    kills = check_move_kill(state, move):

    if kills:
        score = 0

    if not kills and not dead:
        score  = 3

    return score

""" Attempt at a minimax implementation """
def minimax(self, turns):
    """
    minimax boi
    """
    best_value = -1
    best_move_set = None

    starting_state = self.board
    available_moves = get_available_moves(self.board, self.piece_locations, turns)

    all_states = []

    """ Build the tree structure, each node is a potential state of the board,
    that comes from a move made by the player, at this point in time we are at
    the max part of the algorithm  """

    for move in available_moves:
        dead = False

        new_board = self.board
        new_board[move[ROW][ROW]][move[ROW][COL]] = ""

        if self.colour == "black":
            new_board[move[COL][ROW]][move[ROW][COL]] = "@"
        else:
            new_board[move[COL][ROW]][move[COL][COL]] = "O"

        new_state = Board_State(new_board, self.colour, move[ROW], move[COL])
        new_state.opponent_pieces = self.opponent_pieces
        new_state.piece_locations = self.piece_locations

        new_state.piece_locations.remove(move[ROW])
        new_state.piece_locations.append(move[COL])

    if best_value == -1:
        best_value = min_play(new_state, colour, -1)

    opp_score = min_play(new_state, colour, best_value)
    new_state.score = opps_score
        """ We need to now somehow determine the scores of each of the moves here,
        Firstly let's try define some basic score shit lol:
            - Kill is worth 5
            - Getting killed is worth 0
            - Neutral move is worth 2
        current scoring system is fucking shIT
        """

        if check_self_die(new_state, move[COL]):
            dead = True
            score = 0

        if check_move_kill(new_state, move[COL]):
            score = 5

        elif not dead:
            score = 2

        opp_score = min_play(new_state, colour)
        new_state.score = opps_score

        all_states.append(new_state)


    for state in all_states:

        if state.score > best_value:
            best_value = state.score
            best_move_set = (state.old_pos, state.new_pos)

    return best_move_set


def min_play(state, colour):
    """ Form the tree for the opponent now """
    worst_value = 100
    starting_state = state.board
    available_moves = get_available_moves(starting_state, state.opponent_pieces, turns)

    opponents_states = []

    for opp_move in available_moves:
        dead = False

    new_board = starting_state
    new_board[move[ROW][ROW]][move[ROW][COL]] = ""

    if colour == "black":
        new_board[move[COL][ROW]][move[ROW][COL]] = "O"
    else:
        new_board[move[COL][ROW]][move[COL][COL]] = "@"

    new_state = Board_State(new_board, colour, move[ROW], move[COL])
    new_state.opponent_pieces = state.piece_locations
    new_state.piece_locations = state.opponent_pieces

    new_state.piece_locations.remove(move[ROW])
    new_state.piece_locations.append(move[COL])

    new_state.score = evaluation_function(new_state, move[1])

    """ Alpha - Beta Pruning Addition """
    if best_value_found:

        if new_state.score < best_value_found:
            return 0

    """ Scores are reversed as in terms of our player but this is the enemy player's
    fucntion
        - Kill is worth 0
        - Getting killed is worth 5
        - Neutral move is worth 2
    """

    if check_self_die(new_state, move[COL]):
        dead = True
        score = 5

    if check_move_kill(new_state, move[COL]):
        score = 5

    elif not dead:
        score = 2

    next_state.append(new_state)

    if new_state.score <= worst_value:
        worst_value = new_state.score

    return worst_value

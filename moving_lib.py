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
import player as pl
import placing_lib

ROW = 0
COL = 1
MOVEFROM = 0
MOVETO = 1

class Board_State:
  """
  Class that is going to help build our tree for minimax and alpha-beta pruning,
  the class shows all pieces of information relating to that state
  """
  def __init__(self, board, colour, old_pos, new_pos):

    self.board = board
    self.score = None
    self.colour = colour
    self.opponent_locations = None
    self.piece_locations = None
    self.old_pos = old_pos
    self.new_pos = new_pos
    self.moving = True


""" ************************************************************************ """

""" For moving
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):

    move_set = minimax(self, turns)

    return move_set

""" ************************************************************************ """

def get_available_moves(self, turns):
    """
    Function that produces all available moves for the player. The structure of
    the output is a list of nested tuples such that we have (old, new) positions.
    """
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]
    all_moves = []

    for old_pos in self.piece_locations:

        for move in buffers:

            new_pos = (old_pos[ROW] + move[ROW], old_pos[COL] + move[COL])

            if pl.check_legal(self, new_pos, turns):
                all_moves.append((old_pos, new_pos))

    return all_moves

""" ************************************************************************ """

def evaluation_function(state, move):
    """
    Our Evaluation function that determines a score for a specific game state,
    this score is then used within the minimax algorithm to find the optimal play
    """
    score = 0
    dead = False

    if pl.check_self_die(state, move):
        score = 5
        dead = True

    kills = pl.check_move_kill(state, move, state.colour)

    if kills:
        score = 0

    if not kills and not dead:
        score  = 3

    return score

""" ************************************************************************ """

""" Attempt at a minimax implementation """
def minimax(self, turns):
    """
    minimax boi
    """
    best_value = -1
    best_move_set = None

    starting_state = self.board
    available_moves = get_available_moves(self, turns)

    all_states = []

    """ Build the tree structure, each node is a potential state of the board,
    that comes from a move made by the player, at this point in time we are at
    the max part of the algorithm  """

    for move in available_moves:
        dead = False

        new_board = self.board
        new_board[move[MOVEFROM][ROW]][move[MOVETO][COL]] = "-"

        if self.colour == "black":
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "@"
        else:
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "O"

        new_state = Board_State(new_board, self.colour, move[MOVEFROM], move[MOVETO])
        new_state.opponent_locations = self.opponent_locations
        new_state.piece_locations = self.piece_locations

        print(new_state.piece_locations)
        print(move[MOVEFROM])

        new_state.piece_locations.remove(move[MOVEFROM])
        new_state.piece_locations.append(move[MOVETO])

        if best_value == -1:
            best_value = min_play(new_state, self.colour, -1, turns)

        opp_score = min_play(new_state, self.colour, best_value)
        new_state.score = opps_score

        all_states.append(new_state)

        for state in all_states:

            """ We need to now somehow determine the scores of each of the moves here,
            Firstly let's try define some basic score shit lol:
                - Kill is worth 5
                - Getting killed is worth 0
                - Neutral move is worth 2
            current scoring system is fucking shIT
            """

            if pl.check_self_die(new_state, move[MOVETO]):
                dead = True
                score = 0

            if pl.check_move_kill(new_state, move[MOVETO], new_state.colour):
                score = 5

            elif not dead:
                score = 2

                opp_score = min_play(new_state, colour, turns)
                new_state.score = opps_score

                all_states.append(new_state)


        for state in all_states:

            if state.score > best_value:
                best_value = state.score
                best_move_set = (state.old_pos, state.new_pos)

    return best_move_set

""" ************************************************************************ """

def min_play(state, colour, best_value_found, turns):
    """ Form the tree for the opponent now """

    worst_value = 100
    starting_state = state.board
    available_moves = get_available_moves(state, turns)

    opponents_states = []

    for move in available_moves:
        dead = False

        new_board = starting_state
        new_board[move[MOVEFROM][ROW]][move[MOVEFROM][COL]] = "-"

        if colour == "black":
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "O"
        else:
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "@"

        new_state = Board_State(new_board, colour, move[MOVEFROM], move[MOVETO])
        new_state.opponent_locations = state.opponent_locations
        new_state.piece_locations = state.piece_locations

        print(new_state.piece_locations)
        print(move[MOVEFROM])

        new_state.piece_locations.remove(move[MOVEFROM])
        new_state.piece_locations.append(move[MOVETO])

        new_state.score = evaluation_function(new_state, move[MOVETO])

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

        if pl.check_self_die(new_state, move[MOVETO]):
            dead = True
            score = 5

        if pl.check_move_kill(new_state, move[MOVETO], new_state.colour):
            score = 5

        elif not dead:
            score = 2

        next_state.append(new_state) ## What??

        if new_state.score <= worst_value:
            worst_value = new_state.score

    return worst_value

""" ************************************************************************ """

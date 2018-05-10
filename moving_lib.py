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
from numpy import inf

ROW = 0
COL = 1
MOVEFROM = 0
MOVETO = 1

MAX_PIECES = 5
MAX_DEPTH = 4

""" Relative Weights of positions to be used in the evaluation function """
S_TIER = [3,4]
A_TIER = [2,5]
PLEB_TIER = [0,1,6,7]

BEST_SPACE = 5
MID_SPACE = 2
WORST_SPACE = 0

class Board_State:
  """
  Class that is going to help build our tree for minimax and alpha-beta pruning,
  the class shows all pieces of information relating to that state
  """
  def __init__(self, board, colour, old_pos, new_pos):

    self.board = cpy(board)
    # self.score = None
    self.colour = colour
    self.piece_locations = None
    self.opponent_locations = None
    self.old_pos = old_pos
    self.new_pos = new_pos
    self.moving = True


""" ************************************************************************ """

""" For moving
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):

    move_set = alphabetacaller(self, turns)

    return move_set

""" ************************************************************************ """

def get_available_moves(board_state, turns):
    """
    Function that produces all available moves for the player. The structure of
    the output is a list of nested tuples such that we have (old, new) positions.
    """
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]
    all_moves = []

    for old_pos in board_state.piece_locations:

        for move in buffers:

            new_pos = (old_pos[ROW] + move[ROW], old_pos[COL] + move[COL])

            if pl.check_legal(board_state, new_pos, turns):
                all_moves.append((old_pos, new_pos))

            else:
                new_pos_j = (old_pos[ROW] + move[ROW]*2, old_pos[COL] + move[COL]*2)

                if pl.check_legal(board_state, new_pos_j, turns):
                    all_move.append((old_pos, new_pos_j))

    return all_moves

""" ************************************************************************ """

def get_best_moves(board_state, turns):
    """
    Function that gives the moves from the best N pieces on the board.
    N is defined in the moving_lib.py preamble
    Returns:
        best moves: [((fromRow, fromCol), (toRow, toCol)), ...]
    ===================================
    Input Variables:
        board_state:    The Board_State object
        turns:          The number of elapsed turns
    """
    buffers = [(1,0),(-1,0),(0,1),(0,-1)]
    best_moves = []
    best_pieces = []
    best_piece_max_dist = inf

    """ Work out the best N pieces to move """
    for old_pos in board_state.piece_locations:
        man_dist = get_min_dist(old_pos, board_state.opponent_locations)

        if (len(best_pieces) < MAX_PIECES):
            best_pieces.append((old_pos, man_dist))
            best_piece_max_dist = max_move(best_pieces)

        elif man_dist < best_piece_max_dist:
            for piece in best_pieces:
                if best_piece_max_dist == piece[1]:
                    best_pieces.remove(piece)
            best_pieces.append((old_pos, man_dist))
            best_piece_max_dist = max_move(best_pieces)


    for piece in best_pieces:

        for move in buffers:

            new_pos = (piece[0][ROW] + move[ROW], piece[0][COL] + move[COL])

            if pl.check_legal(board_state, new_pos, turns):
                best_moves.append((piece[0], new_pos))

    return best_moves

""" ************************************************************************ """

def max_move(piece_list):
    """
    Determines the maximum value of the pieces which are in form:
        ((row, col), value).
    Returns:
        max_value of the list's values
    ==================================
    Input Variables:
        piece_list: [((row, col), value), ...]
    """

    max_value = -inf

    for piece in piece_list:
        if piece[1] > max_value:
            max_value = piece[1]

    return max_value

""" ************************************************************************ """

def get_min_dist(position, opponent_locations):
    """
    Gets the minimum manhattan distance between the position
    and the opponent_locations.
    Returns:
        minimum manhattan distance
    ==========================
    Input Variables:
        position:   (row, col) position to check from
        opponent_locations: [(row, col), ...] positions of opponent pieces
    """

    min_dist = inf

    for loc in opponent_locations:
        local_min_dist = calc_man_dist(position, loc)
        if local_min_dist < min_dist:
            min_dist = local_min_dist

            return min_dist

""" ************************************************************************* """

def calc_man_dist(piece, pos):
    """
    Calcuates the manhattan distance between 2 positions
    Returns:
        int(Manhattan Distance, (|x1 - x2| + |y1 - y2|))
    ============================
    Input Variabes:
        pos1:         First (row, col) tuple
        pos2:         Second (row, col) tuple
    """
    piece_i = piece[ROW]
    piece_j = piece[COL]
    pos_i = pos[ROW]
    pos_j = pos[COL]

    man_dist = (abs(piece_i - pos_i) + abs(piece_j - pos_j))

    return man_dist


""" ************************************************************************ """

def evaluation_function(board_state):
    """
    Our evaluation function to determine the best moves for our alpha-beta
    pruning implementation,
    Our logic is that we want to be close to the middle of the board so we
    can have ease when the board shrinks so we give higher weights to these
    positions.
    We also want to have ally pieces around us so we aren't easily surrounded
    or we have potential to surround enemy pieces
    Returns:
        relative value of a move based on logic in this function
    ============================
    Input Variables:
        board_state:    Our class holding information about pieces on the board
                        and the potential move
    """


    """ First look at positions of pieces in 3*3 square"""
    move = board_state.new_pos
    ene_count = 0
    ally_count = 0

    if board_state.colour == "black":
        colour = "@"
        ene = "O"
    else:
        colour = "O"
        ene = "@"

    for i in range(3):
        for j in range(3):

            try:
                piece = board_state.board[move[ROW] + i][move[COL] + j]
            except (IndexError, ValueError):
                piece = "-"

            if piece == colour:
                ally_count += 1
            elif piece == ene:
                ene_count += 1

    net_pieces = ally_count - ene_count

    """ Weight the value of the position by relative weights given in global variables """
    net_pos = 0
    pos = [move[ROW], move[COL]]

    for ele in pos:

        if ele in S_TIER:
            net_pos += BEST_SPACE
        elif ele in A_TIER:
            net_pos += MID_SPACE
        elif ele in PLEB_TIER:
            net_pos += WORST_SPACE

    """ Sum these dudes"""

    net_move = net_pos + net_pieces

    """ Losing boards are bad """
    if len(board_state.piece_locations) < 2:
        net_move -= 100

    """ If we die moving into this space, probably not worth the move """

    if pl.check_self_die(board_state, move):
        net_move = 0

    """ If we kill someone we want a big reward to incentivise picking this, this
    must be evaluated after check_self_die as if we kill a piece that could take
    us we technically don't die to due precedence """

    if pl.check_move_kill(board_state, move, board_state.colour):
        net_move = net_pos + net_pieces + 50

    return net_move


""" ************************************************************************ """

def alphabetacaller(player, turn):
    """
    Calls the AlphaBeta recursive algorithm
    Returns:
        Best Move: ((fromRow, fromCol), (roRow, toCol))
    =================================
    Input Variables:
        player:     The player class
        turns:      The number of elapsed turns
    """

    alpha = -inf
    beta = inf
    best_move = ((None, None),(None, None))
    best_val = -inf

    legal_moves = get_best_moves(player, turn)

    for move in legal_moves:
        """ Max recursive call """
        new_board_state = make_move(player, move)
        """ Call a min_play """
        new_best_val = max(best_val,
            alphabeta(new_board_state, MAX_DEPTH, alpha, beta, False, turn))

        """ See if the best move changed """
        if (new_best_val != best_val):
            best_move = move
            best_val = new_best_val

        alpha = max(alpha, best_val)

        if beta <= alpha:
            break

    return best_move

""" ************************************************************************ """

def alphabeta(board_state, depth, alpha, beta, maximPlayer, turn):
    """
    * Based on Pseudocode from:
    https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

    Runs alphabeta pruning recursively until the depth is zero
    Returns:
        best_val := best minimax value
    ===============================
    Input Variables:
        board_state:     The current Board_State object
        depth:      The depth of the current node (0 indicates the end of the run)
        alpha:      The best (move, value) for the max player
        beta:       The best (move, value) for the min player
        maximPlayer: True if the current player is looking for the maximum
    """

    legal_moves = get_best_moves(board_state, turn)

    if (depth == 0) or check_game_over(board_state):
        return evaluation_function(board_state)

    """ Max Play """
    if maximPlayer:
        best_val = -inf
        for move in legal_moves:
            """ Max recursive call """
            new_board_state = make_move(board_state, move)
            best_val = max(best_val,
                alphabeta(new_board_state, depth-1, alpha, beta, False, turn+1))
            alpha = max(alpha, best_val)

            if beta <= alpha:
                break
        return best_val

        """ Min Play """
    else:
        best_val = inf
        for move in legal_moves:
            """ Min recursive call """
            new_board_state = make_move(board_state, move)
            best_val = min(best_val,
                alphabeta(new_board_state, depth-1, alpha, beta, True, turn+1))
            beta = min(beta, best_val)

            if beta <= alpha:
                break
        return best_val

""" ************************************************************************ """

def make_move(board_state, move):
    """
    Creates a new board state after the move has been made.
    Returns:
        Board_State entity
    ======================
    Input Variables:
        board_state:    A Board_State object
        move:           A move ((fromRow, fromCol), (toRow, toCol))
    """
    new_board_state = Board_State(
        cpy(board_state.board), board_state.colour, move[MOVEFROM], move[MOVETO])

    board = new_board_state.board

    board[move[MOVEFROM][ROW]][move[MOVETO][COL]] = "-"

    if new_board_state.colour == "black":
        board[move[MOVETO][ROW]][move[MOVETO][COL]] = "@"
    else:
        board[move[MOVETO][ROW]][move[MOVETO][COL]] = "O"

    new_board_state.piece_locations = board_state.piece_locations[:]
    new_board_state.opponent_locations = board_state.opponent_locations[:]

    new_board_state.piece_locations.remove(move[MOVEFROM])
    new_board_state.piece_locations.append(move[MOVETO])

    new_board_state.new_pos = (move[MOVETO][ROW], move[MOVETO][COL])

    return new_board_state

""" ************************************************************************ """

""" Attempt at a minimax implementation """
def minimax(self, turns):
    """
    # Deprecated
    This works as the max part of our minimax/alpha-beta pruning, what happens
    here is we start to evaluate every potential move and then we check how our
    opponent would react to it and choose the tree branch with the highest evaluation
    score out of all the minimums
    """
    best_value = -1
    best_move_set = None

    starting_state = cpy(self.board)
    available_moves = get_available_moves(self, turns)

    all_states = []

    """ Build the tree structure, each node is a potential state of the board,
    that comes from a move made by the player, at this point in time we are at
    the max part of the algorithm  """

    for move in available_moves:
        dead = False

        new_board = cpy(self.board)
        new_board[move[MOVEFROM][ROW]][move[MOVETO][COL]] = "-"

        if self.colour == "black":
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "@"
        else:
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "O"

        new_state = Board_State(new_board, self.colour, move[MOVEFROM], move[MOVETO])
        new_state.opponent_locations = self.opponent_locations[:]
        new_state.piece_locations = self.piece_locations[:]

        new_state.piece_locations.remove(move[MOVEFROM])
        new_state.piece_locations.append(move[MOVETO])

        if best_value == -1:
            best_value = min_play(new_state, self.colour, -1, turns)

        opp_score = min_play(new_state, self.colour, best_value, turns)
        new_state.score = opp_score

        all_states.append(new_state)

        for state in all_states:

            if state.score >= best_value:
                best_value = state.score
                best_move_set = (state.old_pos, state.new_pos)

    return best_move_set

""" ************************************************************************ """

def min_play(state, colour, best_value_found, turns):
    # Deprecated
    """ Min play we try to determine what the worst play would be for our piece
        from our opponent's perspective, and if we find a lower score than previously
        found we immediately exit out of the function as we shouldn't play
        the move being evaluated in max"""

    worst_value = 100
    starting_state = cpy(state.board)
    available_moves = get_available_moves(state, turns)

    opponents_states = []

    for move in available_moves:
        dead = False

        new_board = cpy(starting_state)
        new_board[move[MOVEFROM][ROW]][move[MOVEFROM][COL]] = "-"

        if colour == "black":
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "O"
        else:
            new_board[move[MOVETO][ROW]][move[MOVETO][COL]] = "@"

        new_state = Board_State(new_board, colour, move[MOVEFROM], move[MOVETO])
        new_state.opponent_locations = state.opponent_locations[:]
        new_state.piece_locations = state.piece_locations[:]

        new_state.piece_locations.remove(move[MOVEFROM])
        new_state.piece_locations.append(move[MOVETO])

        new_state.score = evaluation_function(new_state, move[MOVETO])

        """ Alpha - Beta Pruning Addition """
        if best_value_found:

            if new_state.score < best_value_found:
                return 0

        if new_state.score <= worst_value:
            worst_value = new_state.score

    return worst_value

""" ************************************************************************ """

def cpy(board):
    """
    Makes a copy of the board (rather than referencing)
    """
    return [row[:] for row in board]

""" ************************************************************************ """

def check_game_over(player):
    """
    Returns:
        True if the game is over (regardless of who wins)
    =======================
    Input Variables:
        player:     The player class
    """

    num_opp_pieces = 0
    symb = "O" if (player.colour == "white") else "@"

    for row in player.board:
        for space in row:
            if space == symb:
                num_opp_pieces += 1

    if (num_opp_pieces < 2) or (len(player.piece_locations) < 2):
        return True

    return False

""" ************************************************************************ """

"""****************************************************************************
* player.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
*****************************************************************************"""
from placing_lib import *
from moving_lib import *

""" Index Specifications """
ROW = 0
COL = 1

class Player:
    def __init__(self, colour):
        """
        Called once by the referee to initialise the player. The player builds its
        own board and location representations.
        ============================
        Input Variables:
            self:   Player class as defined in specification
            colour: The player's colour.
        """

        self.colour = colour
        self.board = []
        self.piece_locations = []
        self.opponent_locations = []

        for i in range(8):
            if (i == 0) or (i == 7):
                self.board.append(['X','-','-','-','-','-','-','X'])

            else:
                self.board.append(['-','-','-','-','-','-','-','-'])

    #**************************************************************************

    def action(self, turns):
        """
        Called by referee to request an action from the player.
        Returns:
            move:   Either (row, col) or ((fromRow, fromCol), (toRow, toCol))
        ============================
        Input Variables:
            self:   A Player class as defined in the specification
            turns:  The number of turns taken (incremented by 1 for each move,
                    ie the second round of moves is turns 3 and 4)
        """

        if turns >= 24:
            move = player.moving_phase(self, turns)
        else:
            move = player.placing_phase(self, turns)

        Player.update(self, move)
        return move


    #***************************************************************************

    def update(self, action):
        """
        Called by referee to update your agent of the opponent's actions.
        ==============================
        Input Variables:
            self:   A Player object as defined by the specification
            action: A token move as defined in the specification:
                    Either (col, row) or ((fromCol, fromRow),(toCol, toRow))
        """

        """ Skipped move case """
        if action == None:
            return

        phase = "placing"
        fromSquare = ()
        toSquare = ()

        """ Distinguish a placing from a moving """
        if isinstance(action[0], int):
            toSquare = action
        else:
            fromSquare = action[0]
            toSquare = action[1]
            phase = "moving"


        """ Put the piece in its new location """
        if self.colour == "black":
            self.board[toSquare[COL], toSquare[ROW]] = "O"

        else:
            self.board[toSquare[COL], toSquare[ROW]] = "@"

        self.opponent_locations.append(toSquare)

        """ Remove piece from old location (if applicable) """
        if phase == "moving":
            self.board[fromSquare[COL], fromSquare[ROW]] = "-"
            self.opponent_locations.remove(fromSquare)

""" ************************************************************************* """

def check_legal(player, toPos, turnNum):
    """
    Checks if the proposed move is legal
    Returns:
        True:   if move is legal
        False:  if move is illegal
    ===========================================================================
    Input Variables:
        Player:     A Player object
        toPos:      (row, col)
        turnNum:    The number of turn that it is
    """

    board = player.board

    if player.colour == "white":
        MAX_ROW = 5
        MAX_COL = 7
        MIN_ROW = 0
        MIN_COL = 0

    else:
        MAX_ROW = 7
        MAX_COL = 7
        MIN_ROW = 2
        MIN_COL = 0

    # Number defs
    PLACING = 24
    SHRINK1 = 128
    BRD_BOUND_LOW1 = 1
    BRD_BOUND_HIGH1 = 6
    SHRINK2 = 192
    BRD_BOUND_LOW2 = 2
    BRD_BOUND_HIGH2 = 5

    # Placing Phase Checks
    if turnNum < PLACING:
        # Bounds Check
        #Check Row
        if (toPos[ROW_IDX] > MAX_ROW or toPos[ROW_IDX] < MIN_ROW):
            return False

            # Check Col
        if (toPos[COL_IDX] > MAX_COL or toPos[COL_IDX] < MIN_COL):
            return False

            # Checks on Smallest Board Size
    elif turnNum > SHRINK2:
        # Bounds Check
        # Check Row
        if (toPos[ROW_IDX] > BRD_BOUND_HIGH2 or toPos[ROW_IDX] < BRD_BOUND_LOW2):
            return False

            # Check Col
        if (toPos[COL_IDX] > BRD_BOUND_HIGH2 or toPos[COL_IDX] < BRD_BOUND_LOW2):
            return False

            # Check on first shrink size
    elif turnNum > SHRINK1:
        # Bounds Check
        # Check Row
        if (toPos[ROW_IDX] > BRD_BOUND_HIGH1 or toPos[ROW_IDX] < BRD_BOUND_LOW1):
            return False

            # Check Col
        if (toPos[COL_IDX] > BRD_BOUND_HIGH1 or toPos[COL_IDX] < BRD_BOUND_LOW1):
            return False

        # Check the piece isn't moving into an illegal piece
        # TODO: Check Jump as well
    if (board[toPos[ROW_IDX]][toPos[COL_IDX]] != ""):
        return False

        # Thus the move is legal
    return True


""" ************************************************************************* """

def check_self_die(state, new_pos):
    """
    *** Lifted from Part A Solution

    Check if a potential white move will kill the white piece (to stop the move occurring)
    Returns:        True if white could be killed.
    ________________________
    Input Variables:
        state:      The Board Array as defined above
        new_pos:    The position white is trying to move to.
    """
    piece_i = new_pos[ROW]
    piece_j = new_pos[COL]

    if piece_i == 0 or piece_i == 7:
        if ((state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@")) \
        or (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "X") \
        or (state[piece_i][piece_j + 1] == "X") and (state[piece_i][piece_j - 1] == "@"):

            """ Only need to check left and right of the piece"""

            if (piece_j - 2 < 0):
                pass
            else:
                piece_check = state[piece_i][piece_j - 2]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i][piece_j + 2]

            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    elif piece_j == 0 or piece_j == 7:
        if (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@") \
        or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == "@") \
        or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "X"):

            """ Only need to check above and below of the piece"""

            if (piece_i - 2 < 0):
                pass
            else:
                piece_check = state[piece_i - 2][piece_j]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i + 2][piece_j]

            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    else:


        if (state[piece_i][piece_j + 1] == "@") and (state[piece_i][piece_j - 1] == "@") \
        or (state[piece_i + 1][piece_j] == "@") and (state[piece_i - 1][piece_j] == "@"):

            """ Check left and right """

            if (piece_i - 2 < 0):
                pass
            else:
                piece_check = state[piece_i - 2][piece_j]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i + 2][piece_j]
            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            """ Check above and below"""

            if (piece_j - 2 < 0):
                pass
            else:
                piece_check = state[piece_i][piece_j - 2]

                if piece_check == "O":
                    return False

            try:
                piece_check = state[piece_i][piece_j + 2]
            except IndexError:
                piece_check = False

            if (piece_check == "O"):
                return False

            return True

    return False

""" ************************************************************************* """

def check_move_kill(board, new_pos, colour):
    """
    Alright, let's do some kill confirmed kind of shit now
    """
    buffers = [(1,0), (-1,0), (0,1),(0,-1)]
    kill_count = 0

    if colour == "black":
        sym = "@"
        ene = "O"
    else:
        sym = "O"
        ene = "@"

    for move in bufferss:

        pos_x = new_pos[ROW] + move[ROW]
        pos_y = new_pos[COL] + move[COL]

        pos_2x = new_pos[ROW] + 2*move[ROW]
        pos_2y = new_pos[COL] + 2*move[COL]


    if (pos_x >= 0 and pos_y >= 0) and (pos_2x >= 0 and pos_2y >= 0):

        try:
            piece_e = board[pos_x][pos_y]
            piece_s = board[pos_2x][pos_2y]

            if ((piece_e == ene) and (piece_s == symb or piece_s == "X")):
                kill_count += 1

        except (IndexError, ValueError):
            pass

    return kill_count

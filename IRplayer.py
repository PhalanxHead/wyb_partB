"""****************************************************************************
* irrationalPlayer/player.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: It Begins
*****************************************************************************"""
from IRplacing_lib import *
from IRmoving_lib import *

ROW = 0
COL = 1

class Player:

    def __init__(self, colour):
        # Stuff
        """
        This method is called by the referee once at the beginning of the game to initialise
        our player. You should use this opportunity to set up your own internal
        representation of the board, and any other state you would like to maintain for the
        duration of the game.
        The input parameter colour is a string representing the piece colour your program
        will control for this game. It can take one of only two values: the string 'white' (if
        you are the White player for this game) or the string 'black' (if you are the Black
        player for this game).
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
        # Stuff
        """
        This method is called by the referee to request an action by your player.
        The input parameter turns is an integer representing the number of turns that have
        taken place since the start of the current game phase. For example, if White player
        has already made 10 moves in the moving phase, and Black player has made 10
        moves (and the referee is asking for its 11 th move), then the value of turns would
        be 21.
        Based on the current state of the board, your player should select its next action
        and return it. Your player should represent this action based on the instructions
        below, in the ‘Representing actions’ section.
        """
        """
        From spec:
        Representing actions
            Depending on the current game phase, the actions either player may take on their turn
            may involve placing a piece on a square, moving a piece from one square to another
            or forfeiting their turn. For the purposes of the update() and action()
            methods, we represent each of these actions as follows:
                • To represent the action of placing a piece on square (x,y), use a tuple (x,y).
                • To represent the action of moving a piece from square (a,b) to square (c,d), use
                    a nested tuple ((a,b),(c,d)).
                • To represent a forfeited turn, use the value None.
        """

        if turns >= 24:
            move = IRplayer.moving_phase(self, turns)
        else:
            move = IRplayer.placing_phase(self, turns)

        Player.update(self, move)
        return move


    #***************************************************************************

    def update(self, action):
        # Stuff
        """
        This method is called by the referee to inform your player about the opponent’s
        most recent move, so that you can maintain your internal board configuration.
        The input parameter action is a representation of the opponent’s recent action
        based on the instructions below, in the ‘Representing actions’ section.
        This method should not return anything.
        Note: update() is only called to notify your player about the opponent’s actions.
        Your player will not be notified about its own actions.
        """

        if self.colour == "black":
            self.board[action[COL]][action[ROW]] = "O"

        else:
            self.board[action[COL]][action[ROW]] = "@"

        self.opponent_locations.append(action)


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
    ROW_IDX = 0
    COL_IDX = 1
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
        if (toPos[ROW] > MAX_ROW or toPos[ROW] < MIN_ROW):
            return False

            # Check Col
        if (toPos[COL] > MAX_COL or toPos[COL] < MIN_COL):
            return False

            # Checks on Smallest Board Size
    elif turnNum > SHRINK2:
        # Bounds Check
        # Check Row
        if (toPos[ROW] > BRD_BOUND_HIGH2 or toPos[ROW] < BRD_BOUND_LOW2):
            return False

            # Check Col
        if (toPos[COL] > BRD_BOUND_HIGH2 or toPos[COL] < BRD_BOUND_LOW2):
            return False

            # Check on first shrink size
    elif turnNum > SHRINK1:
        # Bounds Check
        # Check Row
        if (toPos[ROW] > BRD_BOUND_HIGH1 or toPos[ROW] < BRD_BOUND_LOW1):
            return False

            # Check Col
        if (toPos[COL] > BRD_BOUND_HIGH1 or toPos[COL] < BRD_BOUND_LOW1):
            return False

        # Check the piece isn't moving into an illegal piece
        # TODO: Check Jump as well
    if (board[toPos[ROW]][toPos[COL]] != "-"):
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

                if piece_e == ene and (piece_s == symb or piece_s == "X"):
                    kill_count += 1

            except (IndexError, ValueError):
                pass

    return kill_count
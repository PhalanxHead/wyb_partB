"""****************************************************************************
* irrationalPlayer/player.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
*****************************************************************************"""
from IRplacing_lib import *
from IRmoving_lib import *

""" Index Specificaions """
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
        self.moving = False

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
            move:   Either (col, row) or ((fromCol, fromRow), (toCol, toRow))
        ============================
        Input Variables:
            self:   A Player class as defined in the specification
            turns:  The number of turns taken (incremented by 1 for each move,
                    ie the second round of moves is turns 3 and 4)
        """

        """ Check that we haven't entered the moving phase """
        if (turns == 0) and (len(self.opponent_locations) != 0):
            self.moving = True


        if self.moving == True:
            move = IRplayer.moving_phase(self, turns)

        else:
            move = IRplayer.placing_phase(self, turns)

        """ Invert move to keep with spec """
        invertMove(move)

        Player.updateSelf(self, move)
        print("\n Player Board:")
        printBoard(self)

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

        """ Distinguish a placing from a moving """
        if isinstance(action[0], tuple):
            self.moving = True
            fromSquare = action[0]
            toSquare = action[1]
        else:
            toSquare = action

        """ Put the piece in its new location """
        if self.colour == "black":
            self.board[toSquare[COL]][toSquare[ROW]] = "O"

        else:
            self.board[toSquare[COL]][toSquare[ROW]] = "@"

        self.opponent_locations.append(toSquare)

        """ Remove piece from old location (if applicable) """
        if self.moving == True:
            self.board[fromSquare[COL]][fromSquare[ROW]] = "-"
            self.opponent_locations.remove(fromSquare)

        removeDead(self)

    #***************************************************************************

    def updateSelf(self, action):
        """
        Called by Player to update Your own actions.
        ==============================
        Input Variables:
         self:   A Player object as defined by the specification
         action: A token move as defined in the specification:
                 Either (col, row) or ((fromCol, fromRow),(toCol, toRow))
        """

        """ Skipped move case """
        if action == None:
            return

        """ Distinguish a placing from a moving """
        if self.moving == True:
            fromSquare = action[0]
            toSquare = action[1]
        else:
         toSquare = action


        """ Put the piece in its new location """
        if self.colour == "black":
            self.board[toSquare[COL]][toSquare[ROW]] = "@"

        else:
            self.board[toSquare[COL]][toSquare[ROW]] = "O"

        self.piece_locations.append(toSquare)

        """ Remove piece from old location (if applicable) """
        if self.moving == True:
            self.board[fromSquare[COL]][fromSquare[ROW]] = "-"
            self.piece_locations.remove(fromSquare)

        removeDead(self)

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

    """ Boundary Definitions (For placing phase) """
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

    """ Number defs """
    BRD_BOUND_LOW0 = 0
    BRD_BOUND_HIGH0 = 7
    SHRINK1 = 128
    BRD_BOUND_LOW1 = 1
    BRD_BOUND_HIGH1 = 6
    SHRINK2 = 192
    BRD_BOUND_LOW2 = 2
    BRD_BOUND_HIGH2 = 5

    toPos = invertMove(toPos)

    # Placing Phase Checks
    if player.moving == False:
        # Bounds Check
        #Check Row
        if (toPos[ROW] > MAX_ROW or toPos[ROW] < MIN_ROW):
            return False

            # Check Col
        if (toPos[COL] > MAX_COL or toPos[COL] < MIN_COL):
            return False

        # Check largest board size
    elif turnNum < SHRINK1:
        # Bounds Check
        # Check Row
        if (toPos[ROW] > BRD_BOUND_HIGH0 or toPos[ROW] < BRD_BOUND_LOW0):
            return False

            # Check Col
        if (toPos[COL] > BRD_BOUND_HIGH0 or toPos[COL] < BRD_BOUND_LOW0):
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
    else:
        # Bounds Check
        # Check Row
        if (toPos[ROW] > BRD_BOUND_HIGH1 or toPos[ROW] < BRD_BOUND_LOW1):
            return False

            # Check Col
        if (toPos[COL] > BRD_BOUND_HIGH1 or toPos[COL] < BRD_BOUND_LOW1):
            return False

        """ Check the piece isn't moving into an illegal place """
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

""" ************************************************************************* """

def printBoard(player):
    """
    Prints the board
    """
    for col in player.board:
        for row in col:
            print("%s " %row, end='')
        print()
    print("\n")


""" ************************************************************************* """

def invertMove(move):
    """
    Inverts a move from (row, col) to (col, row) (or Vice Versa)
    Or from ((fromCol, fromRow), (toCOl, toRow)) to
    ((fromRow, fromCol), (toRow, toCol))  (or Vice Versa)
    """
    if isinstance(move[0], tuple):
        fromSquare = move[0][::-1]
        toSquare = move[1][::-1]
        move = (fromSquare, toSquare)
    else:
        move = move[::-1]

    return move

""" ************************************************************************* """

def removeDead(player):
    """
    Removes dead pieces from the Board
    =====================
    Input Variables:
        player: the player class
    """
    for piece in player.piece_locations:
        if checkIfDead(player, piece):
            player.piece_locations.remove(piece)
            player.board[piece[COL]][piece[ROW]] = "-"

    for piece in player.opponent_locations:
        if checkIfDead(player, piece):
            player.opponent_locations.remove(piece)
            player.board[piece[COL]][piece[ROW]] = "-"

""" ************************************************************************* """

def checkIfDead(player, piece):
    """
    * Mostly lifted from Part A solution. NOT WORKING. TODO
    Checks if a piece is dead or not.
    Returns:
        True if piece is dead
    =========================
    Input Variables:
        player: As defined in the specification
        piece:  The square of the piece being checked (col, row)
    """

    state = player.board

    if player.colour == "white":
        KS = "O"
    else:
        KS = "@"

    piece_i = piece[ROW]
    piece_j = piece[COL]

    """ Checking if a piece has been killed vertically"""
    if piece_i == 0 or piece_i == 7:
        if (state[piece_i][piece_j + 1] == KS) and (state[piece_i][piece_j - 1] == KS) \
        or (state[piece_i][piece_j + 1] == KS) and (state[piece_i][piece_j - 1] == "X") \
        or (state[piece_i][piece_j + 1] == "X") and (state[piece_i][piece_j - 1] == KS):

            return True

            """ Checking if a piece has been killed horizontally """
    elif piece_j == 0 or piece_j == 7:
        if (state[piece_i + 1][piece_j] == KS) and (state[piece_i - 1][piece_j] == KS) \
        or (state[piece_i + 1][piece_j] == "X") and (state[piece_i - 1][piece_j] == KS) \
        or (state[piece_i + 1][piece_j] == KS) and (state[piece_i - 1][piece_j] == "X"):

            return True

            """ Last Check in case something funny has happened. """
    else:
        if (state[piece_i][piece_j + 1] == KS) and (state[piece_i][piece_j - 1] == KS) \
        or (state[piece_i + 1][piece_j] == KS) and (state[piece_i - 1][piece_j] == KS):

           return True

    return False

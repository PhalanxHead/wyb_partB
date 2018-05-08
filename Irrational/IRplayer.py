"""****************************************************************************
* player.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
*****************************************************************************"""
"""
from placing_lib import *
from moving_lib import *

"""
from IRplacing_lib import *
from IRmoving_lib import *


""" Index Specificaions """
ROW = 0
COL = 1
""" Number Definitions """
SHRINK1 = 128
SHRINK2 = 192


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
        """ Reference as (row, col) """
        self.board = []
        self.piece_locations = []
        self.opponent_locations = []
        self.moving = False
        self.moves = 0

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
        if (turns == 0 or turns == 1) and (len(self.piece_locations) != 0):
            self.moving = True
            self.moves = 0

        if self.moves == SHRINK1:
            print("SHRINKING")
            shrink_board(self, 0)
        elif self.moves == SHRINK2:
            print("SHRINKING")
            shrink_board(self, 1)

        if self.moving == True:
            move = moving_phase(self, turns)

        else:
            move = placing_phase(self, turns)

        """ Invert move to keep with spec """
        move = invert_move(move)

        Player.update(self, move, False)

        return move


    #***************************************************************************

    def update(self, action, oppPlayer=True):
        """
        Called by referee to update your agent of the opponent's actions.
        ==============================
        Input Variables:
            self:   A Player object as defined by the specification
            action: A token move as defined in the specification:
                    Either (col, row) or ((fromCol, fromRow),(toCol, toRow))
            oppPlayer:  True if the move is coming from the opposing player
                        (ie if called by the referee)
        """

        """ Skipped move case """
        if action == None:
            return

        """ Be consistent with board layout """
        action = invert_move(action)

        """ Distinguish a placing from a moving """
        if isinstance(action[0], tuple):
            self.moving = True
            fromSquare = action[0]
            toSquare = action[1]
        else:
            toSquare = action

            """ Check if updating move from the opponent or yourself """
        if oppPlayer:
            """ Select appropriate piece to place """
            placingPiece = "O" if (self.colour == "black") else "@"
            locArray = self.opponent_locations

        else:
            placingPiece = "@" if (self.colour == "black") else "O"
            locArray = self.piece_locations

        self.board[toSquare[ROW]][toSquare[COL]] = placingPiece
        locArray.append(toSquare)


        """ Remove piece from old location (if applicable) """
        if self.moving == True:
            try:
                self.board[fromSquare[ROW]][fromSquare[COL]] = "-"
                locArray.remove(fromSquare)
            except:
                pass

        self.moves += 1

        remove_dead(self, oppPlayer)



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
    BRD_BOUND_LOW1 = 1
    BRD_BOUND_HIGH1 = 6
    BRD_BOUND_LOW2 = 2
    BRD_BOUND_HIGH2 = 5

    # Placing Phase Checks
    if player.moving == False:
        # Bounds Check
        if (toPos[ROW] > MAX_ROW or toPos[ROW] < MIN_ROW) or \
                (toPos[COL] > MAX_COL or toPos[COL] < MIN_COL):
            return False

    # Check largest board size
    elif turnNum < SHRINK1:
        # Bounds Check
        if (toPos[ROW] > BRD_BOUND_HIGH0 or toPos[ROW] < BRD_BOUND_LOW0) or \
                (toPos[COL] > BRD_BOUND_HIGH0 or toPos[COL] < BRD_BOUND_LOW0):
            return False

    # Checks on Smallest Board Size
    elif turnNum >= SHRINK2:
        # Bounds Check
        if (toPos[ROW] > BRD_BOUND_HIGH2 or toPos[ROW] < BRD_BOUND_LOW2) or \
                (toPos[COL] > BRD_BOUND_HIGH2 or toPos[COL] < BRD_BOUND_LOW2):
            return False

    # Check on first shrink size
    else:
        # Bounds Check
        if (toPos[ROW] > BRD_BOUND_HIGH1 or toPos[ROW] < BRD_BOUND_LOW1) or \
                (toPos[COL] > BRD_BOUND_HIGH1 or toPos[COL] < BRD_BOUND_LOW1):
            return False

    """ Check the piece isn't moving into an illegal place """
    # TODO: Check Jump as well
    if (board[toPos[ROW]][toPos[COL]] != "-"):
        return False

    # Thus the move is legal
    return True

""" ************************************************************************* """

def check_self_die(player, new_pos):
    """
    *** Lifted from Part A Solution

    Check if a potential white move will kill the white piece (to stop the move occurring)
    Returns:        True if white could be killed.
    ________________________
    Input Variables:
        state:      The Board Array as defined above
        new_pos:    The position white is trying to move to.
    """
    state = player.board
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

def check_move_kill(player, new_pos, colour):
    """
    Alright, let's do some kill confirmed kind of shit now
    """

    board = player.board

    buffers = [(1,0), (-1,0), (0,1),(0,-1)]
    kill_count = 0

    if colour == "black":
        sym = "@"
        ene = "O"
    else:
        sym = "O"
        ene = "@"

    for move in buffers:

        pos_x = new_pos[ROW] + move[ROW]
        pos_y = new_pos[COL] + move[COL]

        pos_2x = new_pos[ROW] + 2*move[ROW]
        pos_2y = new_pos[COL] + 2*move[COL]


        if (pos_x >= 0 and pos_y >= 0) and (pos_2x >= 0 and pos_2y >= 0):

            try:
                piece_e = board[pos_x][pos_y]
                piece_s = board[pos_2x][pos_2y]

                if piece_e == ene and (piece_s == sym or piece_s == "X"):
                    kill_count += 1

            except (IndexError, ValueError):
                pass

    return kill_count

""" ************************************************************************* """

def invert_move(move):
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

""" ************************************************************************ """

def remove_dead(player, oppPlayer):
    """
    Removes dead pieces from the Board (After player moves)
    =====================
    Input Variables:
        player:     the player class
        oppPlayer:  True if the opponent was the last person to move (ie kill
                        our pieces first)
    """

    if oppPlayer:
        locArray1 = player.piece_locations
        locArray2 = player.opponent_locations
    else:
        locArray1 = player.opponent_locations
        locArray2 = player.piece_locations

    for piece in locArray1:
        if check_if_dead(player, piece):
            locArray1.remove(piece)
            player.board[piece[ROW]][piece[COL]] = "-"

    for piece in locArray2:
        if check_if_dead(player, piece):
            locArray2.remove(piece)
            player.board[piece[ROW]][piece[COL]] = "-"

""" ************************************************************************ """

def check_if_dead(player, piece):
    """
    Checks if a piece is dead or not.
    Returns:
        True if piece is dead
    =========================
    Input Variables:
        player: As defined in the specification
        piece:  The square of the piece being checked (row, col)
    """
    board = player.board
    piece_symb = player.board[piece[ROW]][piece[COL]]
    KS = "OX" if (piece_symb == "@") else "@X"

    BOUND_LOW = 0
    BOUND_HI = 7

    """ Check Outside Columns """
    if (piece[COL] == BOUND_LOW) or (piece[COL] == BOUND_HI):
        if (board[piece[ROW]+1][piece[COL]] in KS) and \
                (board[piece[ROW]-1][piece[COL]] in KS):
            return True

        """ Check Outside Rows """
    elif (piece[ROW] == BOUND_LOW) or (piece[ROW] == BOUND_HI):
        if (board[piece[ROW]][piece[COL]+1] in KS) and \
                (board[piece[ROW]][piece[COL]-1] in KS):
            return True

    else:
        """ Check Vertically """
        if (board[piece[ROW]+1][piece[COL]] in KS) and \
                (board[piece[ROW]-1][piece[COL]] in KS):
            return True

        """ Check Horizontally """
        if (board[piece[ROW]][piece[COL]+1] in KS) and \
                (board[piece[ROW]][piece[COL]-1] in KS):
            return True

    return False

""" ************************************************************************ """

def shrink_board(player, s_num):
    """
    * Adapted from solution in Referee.py

    Shrinks the board when required.
    ======================
    Input Variables:
        player: The player object
        s_num:  Starts at 0 for first shrink. Number of shrinks performed so far
    """
    board = player.board
    s = s_num

    # Remove edges
    for i in range(s, 8 - s):
        for square in [(i, s), (s, i), (i, 7-s), (7-s, i)]:
            x, y = square
            piece = (x,y)
            if piece in player.piece_locations:
                player.piece_locations.remove(piece)
            if piece in player.opponent_locations:
                player.opponent_locations.remove(piece)
            board[x][y] = "-"

    s = s + 1

    # replace the corners (and perform corner elimination)
    for corner in [(s, s), (s, 7-s), (7-s, 7-s), (7-s, s)]:
        x, y = corner
        piece = (x,y)
        if piece in player.piece_locations:
            player.piece_locations.remove(piece)
        if piece in player.opponent_locations:
            player.opponent_locations.remove(piece)
        board[x][y] = 'X'

    remove_dead(player, False)

""" ************************************************************************ """

def print_board(player):
    """
    Prints the board
    """

    print("{} Player's Board:".format(player.colour))
    """ Print the column numbers """
    print("  ", end='')
    for i in range(len(player.board)):
        print("{} ".format(i), end='')
    print()

    row_count = 0
    for col in player.board:
        """ Print the row numbers """
        print("{} ".format(row_count), end='')
        row_count += 1
        """ Print the Squares """
        for square in col:
            print("{} ".format(square), end='')
        print()
    print("\n")

""" ************************************************************************ """

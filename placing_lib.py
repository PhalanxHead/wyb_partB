"""****************************************************************************
* placing_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: - Need an update for board when piece dies
*****************************************************************************"""
import player as pl
import random
from numpy import inf

ROW = 0
COL = 1

TURN_BUFFER = 5
BLACK_STARTING_MOVES = [(4,4), (3,3), (3,4), (4,3), (2,2), (2,3), (2,4), (3,2), (4,2)]
WHITE_STARTING_MOVES = [(4,4), (3,3), (3,4), (4,3), (2,2), (2,3), (2,4), (3,2), (4,2)]


""" ************************************************************************ """

def placing_phase(self, turns):
    """
    Function that determines what the agent should play in the placing phase of the game.
    """

    move = None
    potential_killers = check_if_take(self, turns)

    if len(potential_killers) < 2:
        if self.colour == "black":
            legal_starting = [starting for starting in BLACK_STARTING_MOVES if pl.check_legal(self, starting, turns)]

        else:
            legal_starting = [starting for starting in WHITE_STARTING_MOVES if pl.check_legal(self, starting, turns)]

        if legal_starting:
            move = get_best_placement(self, legal_starting)
        else:
            move = random_place()
            while not pl.check_legal(self, move, turns):
                move = random_place()

    else:
        move = get_best_placement(self, potential_killers)


    return move

""" ************************************************************************ """

def get_best_placement(player, legal_places):
    """
    Gets the best placement based on eval function (1-ply)
    Returns:
        best_place: (row, col)
    ===========================
    Input Variables:
        player:     The player object
        legal_places:   The list of legal places to move to [(row, col), ...]
    """

    best_place = None
    best_val = -inf

    """ Loop through places and get the best place """
    for place in legal_places:
        place_val = place_eval(player, place)

        if place_val > best_val:
            best_place = place
            best_val = place_val


    return best_place

""" ************************************************************************ """

def place_eval(player, move):
    """
    Rates a board.
    net pieces? prioritise centre?
    """
    place_score = 0

    """ At the start we will want to build large gatherings of pieces to
    maximise the chance of our pieces surviving and also taking enemy pieces"""

    ene_count = 0
    ally_count = 0

    if player.colour == "black":
        colour = "@"
        ene = "O"
    else:
        colour = "O"
        ene = "@"

    for i in range(3):
        for j in range(3):

            try:
                piece = player.board[move[ROW]+i][move[COL]+j]
            except (IndexError, ValueError):
                piece = "-"

            if piece == colour:
                ally_count += 1
            elif piece == ene:
                ene_count += 1

    place_score = ally_count - ene_count

    if pl.check_self_die(player, move):
        place_score = 0

    if pl.check_move_kill(player, move, player.colour):
        place_score += 50

    return place_score
    #stub

""" ************************************************************************ """

def check_if_take(self, turns):
    """
    Function to check if there are any opponent's pieces that we could
    possible take out using the placing phase. We look for pieces that have an
    opponents piece next to them, then add these moves if they are valid."""
    potential_move = []

    buffers = [(1,0), (-1,0), (0,1), (0,-1)]

    for piece in self.opponent_locations:

        for i, move in enumerate(buffers, 0):

            #add corner solutions

            if (piece[ROW] + move[ROW], piece[COL] + move[COL]) in self.piece_locations:

                if move == (1,0):
                    new_placement = (piece[ROW] - 1, piece[COL])
                elif move == (-1,0):
                    new_placement = (piece[ROW] + 1, piece[COL])
                elif move == (0,1):
                    new_placement = (piece[ROW], piece[COL] - 1)
                else:
                    new_placement = (piece[ROW], piece[COL] + 1)


                if pl.check_legal(self, new_placement, turns) and \
                                    not pl.check_self_die(self, move):
                    potential_move.append(new_placement)

    return potential_move

"""**************************************************************************"""

def random_place():
    col = random.randint(0,7)
    row = random.randint(0,7)

    return (row, col)

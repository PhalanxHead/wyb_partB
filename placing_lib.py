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
import player
import random

ROW = 0
COL = 1

TURN_BUFFER = 5
BLACK_STARTING_MOVES = []
WHITE_STARTING_MOVES = []


""" ************************************************************************ """

def placing_phase(self, turns):
    """
    Function that determines what the agent should play in the placing phase of the game.
    """

    if turns < TURN_BUFFER:
        """ Choose some initial best moves, here we need to develop a profile of good moves """

        if self.colour == "black":
            legal_starting = [starting for starting in BLACK_STARTING_MOVES if check_legal(self.board, starting, turns)]

        else:
            legal_starting = [starting for starting in WHITE_STARTING_MOVES if check_legal(self.board, starting, turns)]

        if legal_starting:
            move = legal_starting[0]

        else:
            """ Make a random legal move (Just for now) """
            move = random_place()
            while not player.check_legal(self, move, turns):
                move = random_place()
    else:
        """ Maybe be possible to kill the opponent pieces so we want to make a list
            of all these pieces, at the moment if there are multiple pieces, we will take the first """

        potential_killers = check_if_take(self, turns)

        if potential_killers:

            move = potential_killers[0]

        else:
            """ Also making a random move for now. I think controlling the centre
                Will give an advantage though """
            move = random_place()
            while not player.check_legal(self, move, turns):
                move = random_place()
    return move

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


                if player.check_legal(self, new_placement, turns):
                    potential_move.append(new_placement)

    return potential_move

"""**************************************************************************"""

def random_place():
    col = random.randint(0,7)
    row = random.randint(0,5)

    return (row, col)

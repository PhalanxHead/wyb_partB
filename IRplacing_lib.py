"""****************************************************************************
* irrationalPlayer/placing_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: - Need an update for board when piece dies
*****************************************************************************"""
import IRplayer
import random

ROW = 0
COL = 1

def placing_phase(self, turns):
    """
    Function that determines what the agent should play in the placing phase of the game.
    """
    move = random_place()

    """ Make a random legal move """
    while IRplayer.check_legal(self, move, turns) == False:
        move = random_place()

    return move

""" ************************************************************************* """

def random_place():
    """
    Returns a random board position in form (row, col)
    """
    col = random.randint(0,7)
    row = random.randint(0,5)

    return (row, col)

"""****************************************************************************
* player.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: It Begins
*****************************************************************************"""

class player:


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

        self.board = []

      	for i in range(8):
      		if (i == 0) or (i == 7):
      			self.board.append(['X','','','','','','','X'])

      		else:
      			self.board.append(['','','','','','','',''])


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
        	moving_phase(self, turns)

        else:
        	placing_phase(self, turns)

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


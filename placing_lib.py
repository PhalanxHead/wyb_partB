"""****************************************************************************
* placing_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: It Begins
*****************************************************************************"""
""" For placing """
def placing_phase(self, turns):

	potential_killers = check_if_take(self)


	return move


def check_if_take(self):
	""" 
	Function to check if there are any opponent's pieces that we could 
	possible take out using the placing phase. We look for pieces that have an
	opponents piece next to them. Whether the move is valid or not then come in
	later. Returns a list of potential moves that would kill the opponent piece.
	"""

	potential_move = []

	buffers = [(1,0), (-1,0), (0,1), (0,-1)]

	for piece in self.opponent_locations:

		for i, move in enumerate(buffers, 0):

			if (piece[0] + move[0], piece[1] + move[1]) in self.piece_locations:
				
				if move == (1,0):
					new_placement = (piece[0] - 1, piece[1])
				elif move == (-1,0):
					new_placement = (piece[0] + 1, piece[1])
				elif move == (0,1):
					new_placement = (piece[0], piece[1] - 1)
				else:
					new_placement = (piece[0], piece[1] + 1)

				potential_move.append(new_placement)

	return potential_move





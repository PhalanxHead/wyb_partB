"""****************************************************************************
* mvoing_lib.py
* Alistair Moffat Appreciation Society
* Amy Rieck and Luke Hedt
* lhedt@student.unimelb.edu.au
*
* Date: 2018/04/19
*
* Comments: It Begins
*****************************************************************************"""
from player.py import *
from placing_lib import *

class Board_State(board, colour, old_pos, new_pos):
  """
  Class that is going to help build our tree for minimax and alpha-beta pruning,
  the class shows all pieces of information relating to that state
  """
  def __init__(self):

    self.board = board
    self.score = None
    self.colour = colour
    self.opponent_pieces = None
    self.piece_locations = None


""" For moving 
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):



	return (old_pos, new_pos)

def get_available_moves(self, turns):
  """ 
  Function that produces all available moves for the player. The structure of 
  the output is a list of nested tuples such that we have (old, new) positions.
  """
  buffers = [(1,0),(-1,0),(0,1),(0,-1)]
  all_moves = []

  for old_pos in self.piece_locations:

    for move in buffers:

      new_pos = (old_pos[0] + move[0], old_pos[1] + move[1])

      if check_legal(self.board, new_pos, turns):
        all_moves.append((old_pos, new_pos))

  return all_moves 


""" Attempt at a minimax implementation """
def minimax(self, turns):
  """
  minimax boi
  """
  best_value = -1
  starting_state = self.board
  available_moves = get_available_moves(self, turns)

  next_states = []

  """ Build the tree structure, each node is a potential state of the board,
  that comes from a move made by the player """

  for move in available_moves:

    new_board = self.board
    new_board[move[0][0]][move[0][1]] = ""

    if self.colour = "black":
      new_board[move[1][0]][move[0][1]] = "@"
    else:
      new_board[move[1][0]][move[1][1]] = "O"

    new_state = Board_State(new_board, self.colour, move[0], move[1])
    new_state.opponent_pieces = self.opponent_pieces
    new_state.piece_locations = self.piece_locations

   new_state.piece_locations.remove(move[0])
   new_state.piece_locations.append(move[1])

   next_state.append(new_state)

  return (old_pos, new_pos)


# Very Basic Untailored Minimax Implementation
# From http://giocc.com/concise-implementation-of-minimax-through-higher-order-functions.html
def minimax(game_state):
	moves = game_state.get_available_moves()
  	best_move = moves[0]
  	best_score = float('-inf')
  	
  	for move in moves:
		clone = game_state.next_state(move)
    	score = min_play(clone)
    	
    	if score > best_score:
      		best_move = move
      		best_score = score
  
  return best_move

def min_play(game_state):
  	if game_state.is_gameover():
    	return evaluate(game_state)
  
	moves = game_state.get_available_moves()
  	best_score = float('inf')
  	
  	for move in moves:
    	clone = game_state.next_state(move)
    	score = max_play(clone)
    
    	if score < best_score:
      		best_move = move
      	best_score = score
  
  return best_score

def max_play(game_state):
  	if game_state.is_gameover():
    	return evaluate(game_state)
  
  moves = game_state.get_available_moves()
  best_score = float('-inf')
  	
  	for move in moves:
    	clone = game_state.next_state(move)
    	score = min_play(clone)
    
    if score > best_score:
      best_move = move
      best_score = score
  
  return best_score

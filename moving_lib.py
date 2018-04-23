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
    self.old_pos = old_pos
    self.new_pos = new_pos


""" For moving 
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):

    move_set = minimax(self, turns)

    return move_set

def get_available_moves(board, piece_locations, turns):
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
  best_move_set = None

  starting_state = self.board
  available_moves = get_available_moves(self.board, self.piece_locations, turns)

  all_states = []

  """ Build the tree structure, each node is a potential state of the board,
  that comes from a move made by the player, at this point in time we are at
  the max part of the algorithm  """

  for move in available_moves:
    dead = False

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

     """ We need to now somehow determine the scores of each of the moves here,
     Firstly let's try define some basic score shit lol:
     - Kill is worth 5
     - Getting killed is worth 0
     - Neutral move is worth 2
     current scoring system is fucking shIT
     """

    if check_self_die(new_state, move[1]):
      dead = True
      score = 0

    if check_move_kill(new_state, move[1]):
      score = 5

    elif not dead:
      score = 2

    opp_score = min_play(new_state, colour)
    new_state.score = opps_score

    all_states.append(new_state)


  for state in all_states:

    if state.score > best_value:
      best_value = state.score
      best_move_set = (state.old_pos, state.new_pos)

  return best_move_set

def min_play(state, colour):
  """ Form the tree for the opponent now """

  worst_value = 100
  starting_state = state.board
  available_moves = get_available_moves(starting_state, state.opponent_pieces, turns)

  opponents_states = []

  for opp_move in available_moves:
    dead = False

    new_board = starting_state
    new_board[move[0][0]][move[0][1]] = ""

    if colour = "black":
      new_board[move[1][0]][move[0][1]] = "O"
    else:
      new_board[move[1][0]][move[1][1]] = "@"

    new_state = Board_State(new_board, colour, move[0], move[1])
    new_state.opponent_pieces = state.piece_locations
    new_state.piece_locations = state.opponent_pieces

    new_state.piece_locations.remove(move[0])
    new_state.piece_locations.append(move[1])

     """ Scores are reversed as in terms of our player but this is the enemy player's
     fucntion
     - Kill is worth 0
     - Getting killed is worth 5
     - Neutral move is worth 2
     """

    if check_self_die(new_state, move[1]):
      dead = True
      score = 5

    if check_move_kill(new_state, move[1]):
      score = 5

    elif not dead:
      score = 2

    new_state.score = score
    next_state.append(new_state)

    if new_state.score <= worst_value:
      worst_value = new_state.score

  return worst_value

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

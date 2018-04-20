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
""" For moving 
- we want to first use minimax + alpha-beta pruning
- """
def moving_phase(self, turns):



	return (new_pos, old_pos)


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

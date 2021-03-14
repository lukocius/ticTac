#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:22:20 2021

@author: lukocius
"""

import numpy as np


def tic_tac_win_check(board):
    """
    Check if board has a winner.
    Return 0 - incomplete, 1 - has a winner, 2 - full board, but a tie.
    """
    rowsum = np.abs(np.sum(board, axis=0))
    # style comment: refactoring would take longer...
    size = len(board)
    if np.any(rowsum == size):
        return 1
    
    colsum = np.abs(np.sum(board, axis=1))
    if np.any(colsum == size):
        return 1
    
    # diagonal check
    if np.abs(np.trace(board)) == size:
        return 1

    # anti-diagonal
    if np.abs(np.sum(np.flipud(board).diagonal())) == size:
        return 1

    if np.any(board==0):
        return 0
    
    return 2
    

class Board:
    def __init__(self, **kwargs):
        self.size = int(kwargs.get('size', 3))
        # Usually in games it is better to store move history.
        # In this case we use actual board state.
        self.state = np.zeros((self.size**2, self.size**2))
        self._complete_big_squares = np.zeros((self.size, self.size))
        self.current_player = 1
        self.last_move  = -1
        self.availables = np.ones_like(self.state)  # TODO dtype
        self.players = [1, -1]  # TODO needed?

    # TODO state getter. Rename to get_state()    
    def current_state(self):
    
        player_perspective_state = self.current_player*self.state
        return player_perspective_state
    
    def do_move(self, move):
        # Trust the player to do legal moves only!
        if self.availables[move] !=  1:
            raise Exception("Invalid move. Tried to move to: {}".format(move))
        
        self.state[move] = self.current_player
        self.last_move = move
        
        self._local_win_check()
        has_winner = tic_tac_win_check(self._complete_big_squares)
        if has_winner == 2:
            return True, 6
        elif has_winner == 1:
            return True, self.current_player
        
        
        self.current_player *= -1
        self.last_move = move  # 9x9
        self.update_availables()
        
        return False, 6
    
    def update_availables(self):
        cb_x = self.last_move[0]//self.size
        cb_y = self.last_move[1]//self.size
        
        self.availables = np.zeros_like(self.state)
        
        if self._complete_big_squares[cb_x, cb_y]==0:
            self.availables[cb_x:cb_x+self.size,
                              cb_y:cb_y+self.size] = 1-np.abs(
                                  self.state[cb_x:cb_x+self.size,
                                             cb_y:cb_y+self.size])
        else:
            # Move anywhere free space...
            self.availables = 1-np.abs(self.state)
        
        
    def _local_win_check(self):
        # get position!
        cb_x = self.last_move[0]//self.size
        cb_y = self.last_move[1]//self.size
        current_board = self.state[cb_x:cb_x+self.size,
                              cb_y:cb_y+self.size]
        has_winner = tic_tac_win_check(current_board)
        
        # Fill board
        if has_winner != 0:

            if has_winner == 1:
                value = self.current_player
                self.state[cb_x:cb_x+self.size,
                           cb_y:cb_y+self.size] = self.current_player
            elif has_winner == 2:
                value = 6

            self._complete_big_squares[cb_x, cb_y] = value

        return has_winner
        
    def _global_win_check(self):
        has_winner = tic_tac_win_check(self._complete_big_squares)
        return has_winner
    
    
class Game:
    def __init__(self, board=None):
        if board is None:
            self.board = Board()
        else:
            self.board = board
        
    def start_self_play(self, player, is_shown=0, temp=1e-3):
        """ 
        """
        p1, p2 = self.board.players
        states, mcts_probs, current_players = [], [], []
        while True:
            move, move_probs = player.get_action(self.board,
                                                 temp=temp,
                                                 return_prob=1)
            # store the data
            states.append(self.board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.board.current_player)
            # perform a move


            end, winner = self.board.do_move(move)
            if end:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != 6:
                    winners_z[np.array(current_players) == winner] = 1.0
                    winners_z[np.array(current_players) != winner] = -1.0
                # reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game end. Winner is player:", winner)
                    else:
                        print("Game end. Tie")
                return winner, zip(states, mcts_probs, winners_z)    
    
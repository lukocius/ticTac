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
    if np.any(rowsum == 3):
        return 1
    
    colsum = np.abs(np.sum(board, axis=1))
    if np.any(colsum == 3):
        return 1
    
    # diagonal check
    if np.abs(np.trace(board)) == 3:
        return 1

    # anti-diagonal
    if np.abs(np.sum(np.flipud(board).diagonal())) == 3:
        return 1

    if np.any(board==0):
        return 2
    
    return 0
    

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
        self.players = [1, 2]  # TODO needed?

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
                
        
        self.current_player *= -1
        self.last_move = move
        self.availables = self.update_availables(self.last_move)
    
    def update_availables(self):
        pass
    
        
    def _local_win_check(self):
        # get position!
        cb_x = self.last_move[0]//self.size
        cb_y = self.last_move[1]//self.size
        current_board = self.state[cb_x:cb_x+self.size,
                              cb_y:cb_y+self.size]
        has_winner = tic_tac_win_check(current_board)
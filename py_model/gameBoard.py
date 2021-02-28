#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 17:22:20 2021

@author: lukocius
"""

import numpy as np


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
        self.current_player *= -1
        self.last_move = move
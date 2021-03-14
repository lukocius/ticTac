#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 12:51:01 2021

@author: lukocius
Pipeline for model playing model training.
"""

from tictacnet import network
from gameBoard import Board
from collections import deque

class TrainingPipeline:
    """
    
    """
    def __init__(self,
                 model_path=None,
                 board_size=3,
                 batch_size=64):
        
        self.batch_size = batch_size
        self.board_size = board_size
        self.load_model(model_path)
        self.board = Board()
        
    def load_model(self, model_path):
        if model_path is None:
            self.network = network.create_new(self.board_size)
        else:
            self.network = network.load(self.board_size, model_path)    
        
    def _collect_play_data(self, game_batch_size=64):
        for i in range(game_batch_size):
            winner, play_data = self.game.start_self_play(self.mcts_player)
            # Add data to....
            play_data = self.deque()
        
    def train(self):
        try:
            self._collect_self_play_data(self.batch_size)
            
        except KeyboardInterrupt:
            print("\x1b[31mStopped\x1b[0m")

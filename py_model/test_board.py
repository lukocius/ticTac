#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 19:33:35 2021

@author: lukocius
"""

from gameBoard import Board, tic_tac_win_check
import numpy as np
import pytest


def test_win_anti():
    state = np.array([[0, 0, 1],
             [0, 1, -1],
             [1, -1, -1]])
    assert (tic_tac_win_check(state) == 1)
    
    
def test_empty_4():
    state = np.array([[0, 0, 1, -1],
             [0, 1, -1, 0],
             [1, -1, -1, 1],
             [1, 1, 0, -1]])
    assert (tic_tac_win_check(state) == 0)
    

def test_Board():
    board = Board()
    board.do_move((1,1))
    assert board.state[1,1] == 1
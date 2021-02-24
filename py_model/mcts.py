#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 14:50:50 2021

@author: neuro
"""

#from multiprocessing import Pool
# Network s already multiprocessing... With nodes,
# hmmm, write in C and use swig.
import numpy as np
import copy


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class TreeNode:
    # Keep information about probability, value, counts
    def __init__(self, parent, prior_probability):
        self._parent = parent
        self._children = {}  # acton to tree node.
        self._n_visits = 0  # exploration/exploitation parameter
        self._Q = 0
        self._u = 0
        self._P = prior_probability
    
    def expand(self, action_priors):
        """
        Expand tree with probabilities for each action.
        Taking action != adding children.
        Action is chosen from children...
        """
        for action, p in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, p)
    
    def select(self, c_puct):
        """
        Choose children with the best adjusted value.
        """
        return max(self._children.items(),
            key = lambda act_node: act_node[1].get_value(c_puct))
    
    def get_value(self, c_puct):
        # Alpha zero MCTS parameter.
        # polynomial upper confidense bound
        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u
    
    
    def update(self, leaf_value):
        """Update node values from leaf evaluation.
        leaf_value: the value of subtree evaluation from the current player's
            perspective.
        """
        # Count visit.
        self._n_visits += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)
        
    
    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded)."""
        return self._children == {}

    def is_root(self):
        return self._parent is None 
        
    
class MCTS:
    def __init__(self,
                 policy_value_network,
                 c_puct=5,
                 n_playout=10000):
        """
        Policy_value_network returns action-probability (policy)
        and estimate [-1, 1] to win for current player.
        """
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_network
        self._c_puct = c_puct
        self._n_playout = n_playout
    
    def _playout(self, state):
        # Playout. Use copy of the state.
        

        # Greedily choose actions to the end of the current state
        # of the game...
        node = self._root       
        while(1):
            if node.is_leaf():
                break
            action, node = node.select(self._c_puct)
            state.do_move(action)
        
        # Checking for the final winning move might help.
        # Network should learn by itself anyway...
        action_probs, leaf_value = self._policy(state)
        

        end, winner = state.game_end()
        # winner == 1 if last player to move won,
        # 0 if tie. 
        if not end:
            node.expand(action_probs)
            
        if winner == -1:
            leaf_value = 0.0
        else:
            leaf_value = -1.0
            if winner == state.get_current_player():
                leaf_value = 1.0
        # Update whole tree branch
        node.update_recursive(-leaf_value)
        
        
    def get_move_probs(self, state, temp=1e-3):
        for n in range(self._n_playout):
            state_copy = copy.deepcopy(state)
            self._playout(state_copy)
        
        act_visits = [(act, node._n_visits)
                      for act, node in self._root._children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs
    
    
    def update_with_move(self, last_move):
        """Step forward in the tree, keeping everything we already know
        about the subtree.
        """
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, 1.0)

    def __str__(self):
        return "MCTS"
    

class MCTSPlayer(object):
    """AI player based on MCTS"""

    def __init__(self, policy_value_function,
                 c_puct=5, n_playout=2000, is_selfplay=0):
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self._is_selfplay = is_selfplay

    def set_player_ind(self, p):
        self.player = p

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def get_action(self, board, temp=1e-3, return_prob=0):
        sensible_moves = board.availables
        # the pi vector returned by MCTS as in the alphaGo Zero paper
        move_probs = np.zeros(board.width*board.height)
        if len(sensible_moves) > 0:
            acts, probs = self.mcts.get_move_probs(board, temp)
            move_probs[list(acts)] = probs
            if self._is_selfplay:
                # add Dirichlet Noise for exploration (needed for
                # self-play training)
                move = np.random.choice(
                    acts,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                # update the root node and reuse the search tree
                self.mcts.update_with_move(move)
            else:
                # with the default temp=1e-3, it is almost equivalent
                # to choosing the move with the highest prob
                move = np.random.choice(acts, p=probs)
                # reset the root node
                self.mcts.update_with_move(-1)

            if return_prob:
                return move, move_probs
            else:
                return move
        else:
            print("WARNING: the board is full")

    def __str__(self):
        return "MCTS {}".format(self.player)
    
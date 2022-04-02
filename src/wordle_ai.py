# ------------------------------------------------------------------------------
# wordle_ai.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

"""
Possible optimizations:
- save keep_map and remove_map as attributes and
    append new discovered values instead of repetitively
    (up to 6 times) computing this info
"""

# Python imports
from ctypes import pointer
from enum import Enum
from typing import GameState, List

class LetterState(Enum):
    GREY    = 0
    YELLOW  = 1
    GREEN   = 2

class WordleAI:

    def __init__(self, words: set):
        self.possible_words = words

    def prune_words(self, game_state: GameState):
        """
        Prune words from the set of words.

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        """
        keep_map = self._get_keep_map(game_state)
        remove_map = self._get_remove_map(game_state)
        for word in self.possible_words:
            to_remove = False
            for position in range(len(word)):
                letter = word[position]

                # Remove words where letter->position combo are in remove_map
                if letter in remove_map and position in remove_map[letter]:
                    to_remove = True

                # Remove words where position->letter are not in keep_map
                if keep_map[position] != [] and letter not in keep_map[position]:
                    to_remove = True

            if to_remove:
                self.possible_words.remove(word)
        

    def _get_keep_map(self, game_state: dict) -> dict:
        """
        Gets position->letters list MAP describing criteria 
        of words to not prune

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): critieria of words to not prune
        """
        keep_map = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: []
        }
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.GREEN:
                # add letter to position's list
                # Q: should I also add to all other positions?
                if letter not in keep_map[position]: keep_map[position].append(letter)
            
            if state == LetterState.YELLOW:
                # add letter to all other positions' lists
                for i in range(0, 5):
                    if i != position:
                        if letter not in keep_map[position]: keep_map[i].append(letter)
            
        return keep_map
    
    def _get_remove_map(self, game_state) -> dict:
        """
        Gets letter->positions list MAP describing criteria of
        words to prune

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): criteria of words to prune
        """
        remove_map = {}
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.YELLOW:
                # Remove letter for single position
                if letter not in remove_map:
                    remove_map[letter] = []
                remove_map[letter].append(position)

            if state == LetterState.GREY:
                # Remove letter for all positions
                if letter not in remove_map:
                    remove_map[letter] = []
                remove_map[letter] += [0,1,2,3,4]
        
        return remove_map


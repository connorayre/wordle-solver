# ------------------------------------------------------------------------------
# test_wordle_ai.py
#
# April 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

# Python imports
import unittest
from src.wordle_ai import *

class TestWordleAI(unittest.TestCase):

    def test_1_prune_words(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        # Any word with u,c,k,s shall be removed
        input_word_set = {
            "avoid",
            "avoir",
            "avons",
            "avunt"
        }

        expected_output_set = {
            "avoid",
            "avoir",
            "avons",
        }
        
        game_state = [
            {'letter':'d', 'state':LetterState.YELLOW.value, 'position':0},
            {'letter':'u', 'state':LetterState.GREY.value, 'position':1},
            {'letter':'c', 'state':LetterState.GREY.value, 'position':2},
            {'letter':'k', 'state':LetterState.GREY.value, 'position':3},
            {'letter':'s', 'state':LetterState.GREY.value, 'position':4}
        ]
        ai = WordleAI(input_word_set)
        self.assertEqual(expected_output_set, ai.possible_words)
        ai.prune_words(game_state)
        self.assertEqual(expected_output_set, ai.possible_words)
        


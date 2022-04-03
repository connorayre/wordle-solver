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

    def setUp(self) -> None:
        self.word_set_1 = {
            "avoid",
            "avoir",
            "avons",
            "avunt"
        }

        self.game_state_1 = [
            {'letter':'d', 'state':LetterState.YELLOW.value, 'position':0},
            {'letter':'u', 'state':LetterState.EMPTY.value, 'position':1},
            {'letter':'c', 'state':LetterState.EMPTY.value, 'position':2},
            {'letter':'k', 'state':LetterState.EMPTY.value, 'position':3},
            {'letter':'s', 'state':LetterState.EMPTY.value, 'position':4}
        ]

    def test_1_prune_words(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        # Any word with u,c,k,s shall be removed
        #import pdb; pdb.set_trace()

        expected_output_set = {
            "avoid",
            "avoir",
            "avons",
        }
     
        ai = WordleAI(self.word_set_1)
        ai.prune_words(self.game_state_1)  # error: 'avunt' is not getting removed
        self.assertEqual(expected_output_set, ai.possible_words)
        
    def test_2_get_remove_map(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        expected_output = {
            'd':[0],
            'u':[0,1,2,3,4],
            'c':[0,1,2,3,4],
            'k':[0,1,2,3,4],
            's':[0,1,2,3,4]
        }

        ai = WordleAI(self.word_set_1)
        self.assertEqual(expected_output, ai._get_remove_map(self.game_state_1))


    def test_3_get_keep_map(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        expected_output = {
            0:[],
            1:['d'],
            2:['d'],
            3:['d'],
            4:['d']
        }

        ai = WordleAI(self.word_set_1)
        self.assertEqual(expected_output, ai._get_keep_map(self.game_state_1))


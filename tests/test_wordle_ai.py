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
    """
    TODO: test with multi-occurring letter answer word and guess(es)
    Example test words:
        - DODDY
    """

    def setUp(self) -> None:
        self.word_set_1 = {
            "avoid",
            "avoir",
            "avons",
            "avunt"
        }

        # Guessed word(s): ducks
        # Answer: avoid
        self.game_state_1 = [
            {'letter':'d', 'state':LetterState.YELLOW, 'position':0},
            {'letter':'u', 'state':LetterState.EMPTY, 'position':1},
            {'letter':'c', 'state':LetterState.EMPTY, 'position':2},
            {'letter':'k', 'state':LetterState.EMPTY, 'position':3},
            {'letter':'s', 'state':LetterState.EMPTY, 'position':4}
        ]

    def test_1_prune_words(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        # Any word with u,c,k,s shall be removed
        # AND
        # Any word with d shall be kept

        expected_output_set = {
            "avoid"
        }
     
        ai = WordleAI(self.word_set_1)
        ai.prune_words(self.game_state_1)  # error: 'avunt' is not getting removed
        print(ai.possible_words, expected_output_set)
        self.assertEqual(ai.possible_words, expected_output_set)
        
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
        self.assertEqual(ai._get_remove_map(self.game_state_1), expected_output)


    def test_3_get_keep_map(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        expected_output = {
            0:[],
            1:[],
            2:[],
            3:[],
            4:[]
        }

        #import pdb; pdb.set_trace()
        ai = WordleAI(self.word_set_1)
        self.assertEqual(ai._get_keep_map(self.game_state_1), expected_output)

    def test_4_get_yellow_set(self):
        # Target answer: avoid
        # Guessed word(s): ducks
        expected_output = {'d'}

        ai = WordleAI(self.word_set_1)
        self.assertEqual(ai._get_yellow_set(self.game_state_1), expected_output)


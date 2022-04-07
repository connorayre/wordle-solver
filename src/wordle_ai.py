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
from enum import Enum
from typing import List
import math
from wordle_db import words
from string import ascii_lowercase
from pprint import pprint

class LetterState(Enum):
    EMPTY    = 0
    YELLOW  = 1
    GREEN   = 2

class WordleAI:

    def __init__(self, wordset: set):
        if wordset is None:
            wordset = words 
        self.possible_words = set(wordset)

    def prune_words(self, game_state):
        """
        Prune words from the set of words.

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        """
        keep_map = self._get_keep_map(game_state)
        remove_map = self._get_remove_map(game_state)
        yellow_set = self._get_yellow_set(game_state)
        removed_words = set()
        for word in self.possible_words:
            to_remove = False
            temp_set = yellow_set.copy()    # if this set is not empty after all word letters, remove word
                                            # how does this handle multi-occurring letters?
            for position in range(len(word)):
                letter = word[position]

                if letter in keep_map[position]:
                    # Letter at position is known and letter is correct
                    break
                elif keep_map[position] == []:
                    # Letter at position is not known yet
                    pass
                else:
                    # Letter at position is known and letter is not correct
                    to_remove = True
                    break
                
                if letter not in remove_map or position not in remove_map[letter]:
                    # We don't know if letter is not at the position and we
                    #   also don't know if it is at that position
                    pass
                else:
                    # Letter is known to not be at position
                    to_remove = True
                    break

                if letter in temp_set:
                    temp_set.remove(letter)

            if len(temp_set) > 0:
                to_remove = True

            if to_remove:
                #self.possible_words.remove(word)
                removed_words.add(word)
        
        self.possible_words = self.possible_words - removed_words        

    def _get_keep_map(self, game_state: dict) -> dict:
        """
        Gets position->letters list MAP describing criteria 
        of words to not prune

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): critieria of words to not prune
        """
        # TODO: I need to account for when the map is updated with new info
        keep_map = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: []
        }
        is_locked = [False for i in range(5)]

        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.GREEN:
                # add letter to position's list
                # Remove all other letters at position and add letter
                keep_map[position] = [letter]
                # Switch lock for position on to prevent other letters
                #   from being added to the position's list
                is_locked[position] = True
            
        return keep_map

    def _get_yellow_set(self, game_state):
        """
        Gets set of letters whose positions are unknown
        but are known to be in the final word
        """
        yellow_set = set()
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.YELLOW:
                # add letter to yellow set
                if letter not in yellow_set: yellow_set.add(letter)
        
        return yellow_set


    def prune_words_v2(self, game_state):
        filter = self._get_position_letter_map(game_state)
        pprint(f"filter map:\n{filter}")
        removed_words = set()
        for word in self.possible_words:
            for i, letter in enumerate(word):
                if letter not in filter[i]:
                    removed_words.add(word)
                    break
            
        self.possible_words = self.possible_words - removed_words


    def _get_position_letter_map(self, game_state):

        pos_letter_map = {
            0:{letter for letter in ascii_lowercase},
            1:{letter for letter in ascii_lowercase},
            2:{letter for letter in ascii_lowercase},
            3:{letter for letter in ascii_lowercase},
            4:{letter for letter in ascii_lowercase}
        }

        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.GREEN:
                # Remove all other letters at position
                pos_letter_map[position] = [letter]

            if state == LetterState.YELLOW:
                # Remove letter at position
                if letter in pos_letter_map[position]:
                    pos_letter_map[position].remove(letter)

            if state == LetterState.EMPTY:
                # Remove letter at all positions
                for pos in range(5):
                    if letter in pos_letter_map[pos]:
                        pos_letter_map[pos].remove(letter)

        return pos_letter_map
    
    def _get_remove_map(self, game_state) -> dict:
        """
        Gets letter->positions list MAP describing criteria of
        words to prune.

        When a grey letter is found, the letter is marked to be
        removed on

        Args:
            - game_state ('List[dict]): list of dictionaries describing guess outcomes
        Returns:
            - ('dict'): criteria of words to prune
        """
        # TODO: I need to account for when the map is updated with new info
        remove_map = {}
        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']

            if state == LetterState.YELLOW:
                # Remove letter for single position
                if letter not in remove_map:
                    remove_map[letter] = []
                if position not in remove_map[letter]: remove_map[letter].append(position)

            if state == LetterState.EMPTY:
                # Remove letter for all positions
                if letter not in remove_map:
                    remove_map[letter] = []
                for i in range(5):
                    if i not in remove_map[letter]: remove_map[letter] += [i]
        
        return remove_map

    #***********************************************************************************************************
    #function to calculate entropy (expected value of information), returns a float
    #Args:
    #     - word: (Str) word that the entropy is being calculated on, based on self.possible_words
    #     - game_state: (not used)
    def calculate_entropy(self, word, game_state=None) -> float:
        #initialize wordCount, entropy and single word array that contains a dictionary with letter and state
        entropy = 0.0
        wordCount = 0
        probability = 0.0
        information = 0.0
        state_word = [{ "letter": word[0],  "state": LetterState.EMPTY},
                       { "letter": word[1],  "state": LetterState.EMPTY},
                       { "letter": word[2],  "state": LetterState.EMPTY},
                       { "letter": word[3],  "state": LetterState.EMPTY},
                       { "letter": word[4],  "state": LetterState.EMPTY}
                      ]
                      
        #iterate over each possible state that the word can have
        #for each state, find out how many words would be left in remainingwords
        #then calculate p(x) * log base 2 (1/p(x)) and add it to entropy
        # p(x) = possible_matches_with_state / len(remaining words)
        #ie: "for state in range(0,243)"
        for state1 in range(0,3):
            for state2 in range(0,3):
                for state3 in range(0,3):
                    for state4 in range(0,3):
                        for state5 in range(0,3):
                            #initialize to next possible state
                            state_word[0]["state"] = LetterState(state1)
                            state_word[1]["state"] = LetterState(state2)
                            state_word[2]["state"] = LetterState(state3)
                            state_word[3]["state"] = LetterState(state4)
                            state_word[4]["state"] = LetterState(state5)

                            
                            #go over remaining words and if they fit under the current state, add 1 to wordcount
                            #this for loop is calculating the numerator for our p(x)
                            for remaining_word in self.possible_words:
                                #-------------------------------------------
                                #if our state says a certain letter is not in
                                #the answer word (ie: LetterState = EMPTY), then if the remaining_word
                                #contains that letter, we dont include the word in wordCount

                                #(LetterState = EMPTY)
                                if(state_word[0]["state"] == LetterState.EMPTY):
                                    if(state_word[0]["letter"] in remaining_word):
                                        continue
                                if(state_word[1]["state"] == LetterState.EMPTY):
                                    if(state_word[1]["letter"] in remaining_word):
                                        continue
                                if(state_word[2]["state"] == LetterState.EMPTY):
                                    if(state_word[2]["letter"] in remaining_word):
                                        continue
                                if(state_word[3]["state"] == LetterState.EMPTY):
                                    if(state_word[3]["letter"] in remaining_word):
                                        continue
                                if(state_word[4]["state"] == LetterState.EMPTY):
                                    if(state_word[4]["letter"] in remaining_word):
                                        continue
                                #-------------------------------------------
                                #our state says our answer word contains the letter,
                                #just not in the current location (ie: LetterState = YELLOW)
                                #so if the word contains the letter in that location
                                #continue, or if the letter is not in the word
                                #altogether then continue

                                #(LetterState = YELLOW)
                                if(state_word[0]["state"] == LetterState.YELLOW):
                                    if(remaining_word[0] == state_word[0]["letter"]):
                                        continue
                                    if(not state_word[0]["letter"] in remaining_word):
                                        continue
                                if(state_word[1]["state"] == LetterState.YELLOW):
                                    if(remaining_word[1] == state_word[1]["letter"]):
                                        continue
                                    if(not state_word[1]["letter"] in remaining_word):
                                        continue
                                if(state_word[2]["state"] == LetterState.YELLOW):
                                    if(remaining_word[2] == state_word[2]["letter"]):
                                        continue
                                    if(not state_word[2]["letter"] in remaining_word):
                                        continue
                                if(state_word[3]["state"] == LetterState.YELLOW):
                                    if(remaining_word[3] == state_word[3]["letter"]):
                                        continue
                                    if(not state_word[3]["letter"] in remaining_word):
                                        continue
                                if(state_word[4]["state"] == LetterState.YELLOW):
                                    if(remaining_word[4] == state_word[4]["letter"]):
                                        continue
                                    if(not state_word[4]["letter"] in remaining_word):
                                        continue
                                #-------------------------------------------
                                #our state says that the letter is in the correct
                                #position(ie: LetterState = GREEN), so we check if the word has the letter
                                #in the correct position, and if not continue

                                #(LetterState = GREEN)
                                if(state_word[0]["state"] == LetterState.GREEN):
                                    if(not remaining_word[0] == state_word[0]["letter"]):
                                        continue
                                if(state_word[1]["state"] == LetterState.GREEN):
                                    if(not remaining_word[1] == state_word[1]["letter"]):
                                        continue
                                if(state_word[2]["state"] == LetterState.GREEN):
                                    if(not remaining_word[2] == state_word[2]["letter"]):
                                        continue
                                if(state_word[3]["state"] == LetterState.GREEN):
                                    if(not remaining_word[3] == state_word[3]["letter"]):
                                        continue
                                if(state_word[4]["state"] == LetterState.GREEN):
                                    if(not remaining_word[4] == state_word[4]["letter"]):
                                        continue
                                #if we make it to this point, then the remaining_word from self.possible_words is a possibility for that state
                                #so we increase wordcount
                                wordCount += 1

                            #calculate the probability for this given state
                            probability = (wordCount/len(self.possible_words))
                            #in the case probability is 0, just continue
                            if(probability == 0):
                               continue
                            #calculate the information and add it to entropy
                            information = (probability) * (math.log2(1/probability))
                            entropy = entropy + information

                            #reset word count
                            wordCount = 0
        return entropy


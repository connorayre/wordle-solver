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
# from wordle_db3 import wordset as words
from string import ascii_lowercase
from pprint import pprint
from frequency_map import frequency_map
import numpy as np
import itertools
import json

class LetterState(Enum):
    EMPTY    = 0
    YELLOW  = 1
    GREEN   = 2

class WordleAI:

    def __init__(self, wordset: set):
        with open("word_indices.json", "r") as outfile:
          self.word_indices = json.load(outfile)
        if wordset is None:
            wordset = words 
        self.possible_words = set(wordset)        

    def prune_words_v2(self, game_state):
        filter = self._get_position_letter_map(game_state)
        #pprint(f"filter map:\n{filter}")
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
        locks = {i: False for i in range(5)}

        for guess in game_state:
            letter = guess['letter']
            state = guess['state']
            position = guess['position']
            if state is LetterState.GREEN:
                # Remove all other letters at position
                locks[position] = True
                pos_letter_map[position] = {letter}
                continue

            if state is LetterState.YELLOW:
                # Remove letter at position
                if letter in pos_letter_map[position]:
                    pos_letter_map[position] -= {letter}
                continue

            if state is LetterState.EMPTY:
                # Remove letter at all positions
                # Edit:
                #   - if a letter is marked as empty, remove
                #       it at all NON-LOCKED positions
                for pos in range(5):
                    if not locks[pos]:
                        pos_letter_map[pos] -= {letter}
                continue

        return pos_letter_map
    
    def save_indices(self): 
        indices = dict()
        for i, word in enumerate(words):
            indices[word] = i
        with open("word_indices.json", "w") as outfile:
            json.dump(indices, outfile)
        
        return indices

    def get_state_table(self):
        table = np.zeros((len(words), len(words)))
        
        for i1, i2 in itertools.permutations(range(len(words)), 2):   
            w1 = words[i1]
            w2 = words[i2]
            letter_indices = dict()
            for i, letter in enumerate(w1):
                if letter in letter_indices:
                    letter_indices[letter].add(i)
                else:
                    letter_indices[letter] = set([i])

            guess = 0
            for i, c in enumerate(w2):
                guess *= 10
                if c in letter_indices and i in letter_indices[c]:
                    letter_indices[c].remove(i)
                    guess += LetterState.GREEN.value
                else:
                    guess += LetterState.EMPTY.value

            for i, c in enumerate(w2):
                if (guess // (10**(4-i))) % 10 == 0:
                    if c in letter_indices and len(letter_indices[c]) > 0:
                        guess += LetterState.YELLOW.value * (10**(4-i))  
            
            table[i1, i2] = guess
        
        np.fill_diagonal(table, 22222)
        np.save("pat_table.npy", table)

        return table

    def get_frequencies(self):
        def sigmoid(x):
            return 1 / (1 + math.exp(-x))
        width = 10
        c = width * (-0.5 + 3000 / len(frequency_map.keys()))
        space = np.linspace(c - width / 2, c + width / 2, len(words))
        sorted_words = sorted(frequency_map.items(), key=lambda x: x[1])
        normalized = dict()
        for word, score in zip(sorted_words, space):
            normalized[word[0]] = sigmoid(score)
        self.frequencies = normalized
        return normalized

    def get_word_probabilities(self):
        probs = np.array([self.frequencies[word] for word in self.possible_words])
        tot = probs.sum()
        if tot == 0:
            return np.zeros(probs.shape)
        return probs / tot

    def calculate_entropy_v2(self, word, pattern_table):
        entropy = 0.0
        probability = 0.0
        information = 0.0

        i2 = self.word_indices[word]
        w2 = word

        counter = dict()
        for index, possible_word in enumerate(self.possible_words):
            
            i1 = self.word_indices[possible_word]
            # pattern = pattern_table[i1, i2]
            w1 = possible_word
            letter_indices = dict()
            for i, letter in enumerate(w1):
                if letter in letter_indices:
                    letter_indices[letter].add(i)
                else:
                    letter_indices[letter] = set([i])
            guess = 0
            for i, c in enumerate(w2):
                guess *= 10
                if c in letter_indices and i in letter_indices[c]:
                    letter_indices[c].remove(i)
                    guess += LetterState.GREEN.value
                else:
                    guess += LetterState.EMPTY.value

            for i, c in enumerate(w2):
                if (guess // (10**(4-i))) % 10 == 0:
                    if c in letter_indices and len(letter_indices[c]) > 0:
                        guess += LetterState.YELLOW.value * (10**(4-i))  
            pattern = guess
            
            if pattern not in counter:
                counter[pattern] = 0
            counter[pattern] += 1
        
        for pat in counter:
            probability = (counter[pat]/len(self.possible_words))
            #in the case probability is 0, just continue
            if(probability == 0):
                continue
            #calculate the information and add it to entropy
            information = (probability) * (math.log2(1/probability))
            entropy = entropy + information
        return entropy + self.frequencies[word]


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


# ------------------------------------------------------------------------------
# wordle_solver.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

from wordle_game import WordleGame
from wordle_db import words
from wordle_ai import *
from wordle_api import *
from wordle_db3 import wordset

def old_main():
    # TODO: add word frequency check
    game = WordleGame(words)
    game.start_game()
    ai = WordleAI(words)

    count = 1

    # 1. Insert default first guess
    initial_word = 'crans'
    guessed_word = initial_word
    game.guess_word(initial_word)    # i cannot find crane
    print(f"Guessed {initial_word}")
    while count <= 6 or ai.possible_words == set():
        # TODO: how do I identify that word has been guessed?
        #   - remove guessed word from set, causing
        #       self.possible_words to become empty if word was
        #       guessed?
        # 2. Prune list of words based on result
        ai.prune_words(game.get_state())
        # 3. Calculate entropy for all of the remaining words
        #   and select word with highest entropy
        max_entropy = 0
        guessed_word = None
        for word in ai.possible_words:
            if guessed_word is None:
                # set initial entropy word
                entropy_word = word
            if ai.calculate_entropy(word) > max_entropy:
                # set new word with highest entropy
                entropy_word = word
            
        # 4. Guess word and get result
        if guessed_word is not None:
            print(f"Guessed {guessed_word}")
            game.guess_word(guessed_word)
        # 5. Repeat 2-4 until answer is guessed or 6 guesses
        #   have been made
        count += 1
    
def main():
    game = WordleAPI()
    ai = WordleAI(wordset)

    status = game.start_game()
    # 1. Insert default first guess
    status = game.guess('crane')
    while status == GameStatus.ONGOING:
        # 2. Prune list based on result
        ai.prune_words(game.get_game_state())
        # 3. Calculate entropy for all remaining words and
        #   select word with highest entropy
        max_entropy = 0.0
        next_guess = None

        for word in ai.possible_words:
            if ai.calculate_entropy(word) > max_entropy:
                next_guess = word
        
        # 4. Guess word and get result
        status = game.guess(next_guess)
        # 5. Repeat 2-4 until answer is guessed or max guesses
        #   have been made
    

if __name__ == "__main__":
    main()
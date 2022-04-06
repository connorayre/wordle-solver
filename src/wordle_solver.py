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

def main():
    # TODO: add word frequency check
    game = WordleGame(words)
    game.start_game()
    ai = WordleAI(words)

    count = 1

    # 1. Insert default first guess
    initial_word = 'crans'
    game.guess_word(initial_word)    # i cannot find crane
    print(f"Guessed {initial_word}")
    while count >= 6 or ai.possible_words == set():
        # 2. Prune list of words based on result
        ai.prune_words(game.get_state())
        # 3. Calculate entropy for all of the remaining words
        #   and select word with highest entropy
        max_entropy = 0
        entropy_word = None
        for word in ai.possible_words:
            if entropy_word is None:
                # set initial entropy word
                entropy_word = word
            if ai.calculate_entropy(word) > max_entropy:
                # set new word with highest entropy
                entropy_word = word
            
        # 4. Guess word and get result
        if entropy_word is not None:
            print(f"Guessed {entropy_word}")
            game.guess_word(entropy_word)
        # 5. Repeat 2-4 until answer is guessed or 6 guesses
        #   have been made
        count += 1
    return 0

if __name__ == "__main__":
    main()
# ------------------------------------------------------------------------------
# interactive_solver.py
#
# April 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

# Python libraries
from wordle_ai import *
from wordle_api import *
from wordle_db3 import wordset as wordset3
from wordle_db2 import wordset as wordset2
from wordle_api import GameStatus
from heapq import *


class InteractiveWordle():

    def __init__(self, wordset):
        self.wordset = wordset
        self.status = GameStatus.STARTED
        self.num_guesses = 0
        self.game_state = []
        self.guess_history = []
        self.ai = WordleAI(wordset.copy())

    def start_game(self):
        print("Game started")
        self.status = GameStatus.STARTED
        self.num_guesses = 0
        self.game_state = []
        self.guess_history = []

    def guess_word(self):
        # NOTE: No error-checking implemented
        if self.status is GameStatus.MAX_GUESSES or self.status is GameStatus.ANSWER_FOUND:
            print("ERROR: game has ended")
        print(f"--Guess #{self.num_guesses + 1}--")
        
        self._print_recommended_words()

        guess_input = input("Insert guess: ")
        result_input = input("Input result: ")
        self.guess_history += [guess_input]
        self.game_state += self._format_state(
            self.guess_history[-1], result_input)
        #print(self.ai.possible_words)
        self.ai.prune_words_v2(self.game_state)

        if result_input == 'ggggg':
            self.status = GameStatus.ANSWER_FOUND
        
        self.num_guesses += 1
        if self.num_guesses >= 6 or self.status is GameStatus.ANSWER_FOUND:
            self.end_game()

    def _format_state(self, word, result):
        game_state = []
        state_map = {'g': LetterState.GREEN,
                     'y': LetterState.YELLOW, 'e': LetterState.EMPTY}
        for position, letter in enumerate(word):
            state = state_map[result[position]]
            game_state += [{'letter': letter,
                            'state': state, 'position': position}]
        return game_state

    def _print_recommended_words(self):
        
        entropy_heap = []
        print(f"Recommended words ({len(self.ai.possible_words)} remaining):")
        if self.num_guesses > 0:

            entropy_heap = self._get_entropy_heap()
            # print(f"Entropy heap {entropy_heap}")
            i = 0
            while i < 10 and i < len(entropy_heap):
                # Print 10 words with largest entropies
                popped = heappop(entropy_heap)
                # print(f"popped: {popped}")
                entropy, word = popped
                print(f"- {word}: {entropy * -1}")
                i += 1
        else:
            print("- crane")
        

    def _get_entropy_heap(self):
        entropy_heap = []
        print("calculating entropies...")
        for word in self.ai.possible_words:
            #heappush(entropy_heap, self.ai.calculate_entropy(word))
            #entropy_heap += [self.ai.calculate_entropy(word), word]
            heappush(entropy_heap, (-1 * self.ai.calculate_entropy(word), word))
        # print(entropy_heap)
        return entropy_heap

    def end_game(self):
        print("Game over")
        self.status = GameStatus.MAX_GUESSES


def main():
    game = InteractiveWordle(wordset3)
    game.start_game()
    count = 0
    guess = 0
    answer = -1

    while game.status is not GameStatus.MAX_GUESSES and game.status is not GameStatus.ANSWER_FOUND:
        game.guess_word()

    print("Done.")


if __name__ == "__main__":
    main()

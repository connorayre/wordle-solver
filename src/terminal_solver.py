import numpy as np
from wordle_game import WordleGame
from wordle_api import GameStatus
from wordle_ai import WordleAI
from wordle_db import words
from wordle_db3 import wordset
import heapq
import sys
import json

first_guess = [(-6.19, "tares"), (-6.15, "lares"), (-6.11, "rales"), (-6.10, "rates"), (-6.08, "teras"), (-6.07, "nares"), (-6.06, "soare"), (-6.05, "tales"), (-6.05, "reais"), (-6.03, "tears")]

def main():
  pat_table = np.load("pat_table.npy")
  game = WordleGame(words)
  # game.start_game(input("Answer (press enter for random answer): "))
  ai = WordleAI(words)
  ai.get_frequencies()
  tot = 0
  for answer in wordset[:100]:
    game = WordleGame(words)

    ai.possible_words = set(words)
    game.start_game(answer)
    if "--skip" in sys.argv:
      game.guess("tares")
      ai.prune_words_v2(game.get_game_state())

    while True:
      # print(game)
      # print("Calculating...")

      # print(len(ai.possible_words))
      # if len(ai.possible_words) <= 2:
      #   for word in ai.possible_words:
      #     print(f"{word}: {ai.calculate_entropy_v2(word, pat_table):.2f}")

      top_words = []
      if len(game.get_state()) == 0:
        top_words = first_guess
      else:
        for word in ai.possible_words:
          # heapq.heappush(top_words, (ai.calculate_entropy(word) * -1, word))
          heapq.heappush(top_words, (ai.calculate_entropy_v2(word, pat_table) * -1, word))
      
      # for entropy, word in heapq.nsmallest(10, top_words):
      #   print(f"{word}: {(entropy * -1):.2f}")

      guess = ""
      if "--auto" in sys.argv:
        guess = top_words[0][1]
        # print(f"\nGuess: {guess}\n")
      else:
        guess = input("\nGuess: ")

      if game.guess(guess) != GameStatus.ONGOING:
        break
      
      if len(game.get_state()) > 0:
        ai.prune_words_v2(game.get_game_state())
    
    print(game)
    print(f"Score: {len(game.game_state)}")
    tot += len(game.game_state)
  print(tot/100)
# from pattern_table import pattern_table
if __name__ == "__main__":
  ai = WordleAI(words)
  # ai.get_state_table()
  # print(np.load("pat_table.npy"))
  # ai.save_indices()
  # ai.get_frequencies()
  # pattern_table = dict()
  # with open("pattern_table.json", "r") as outfile:
  #   pattern_table = json.load(outfile)
  #   print("loaded")
  # print(ai.calculate_entropy_v2("tares", np.load("pat_table.npy")))
  # for word in ["tares", "lares", "rales", "rates", "teras", "nares", "soare", "tales", "reais", "tears"]:
  #   print(word, ai.calculate_entropy_v2(word, np.load("pat_table.npy")))
  main()
from wordle_game import WordleGame
from wordle_api import GameStatus
from wordle_ai import WordleAI
from wordle_db import words
import heapq
import sys

first_guess = [(-6.19, "tares"), (-6.15, "lares"), (-6.11, "rales"), (-6.10, "rates"), (-6.08, "teras"), (-6.07, "nares"), (-6.06, "soare"), (-6.05, "tales"), (-6.05, "reais"), (-6.03, "tears")]

def main():
  game = WordleGame(words)
  game.start_game(input("Answer (press enter for random answer): "))
  ai = WordleAI(words)

  while True:
    print(game)
    print("Calculating...")

    top_words = []
    if len(game.get_state()) == 0:
      top_words = first_guess
    else:
      for word in ai.possible_words:
        heapq.heappush(top_words, (ai.calculate_entropy(word) * -1, word))
    
    for entropy, word in heapq.nsmallest(10, top_words):
      print(f"{word}: {(entropy * -1):.2f}")

    guess = ""
    if "--auto" in sys.argv:
      guess = top_words[0][1]
      print(f"\nGuess: {guess}\n")
    else:
      guess = input("\nGuess: ")

    if game.guess(guess) != GameStatus.ONGOING:
      break
    
    if len(game.get_state()) > 0:
      ai.prune_words_v2(game.get_game_state())
  
  print(game)
  print(f"Answer: {game.answer}")

if __name__ == "__main__":
  # ai = WordleAI(words)
  # print(ai.calculate_entropy_v2("store"))
  main()
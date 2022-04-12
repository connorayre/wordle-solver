from wordle_game import WordleGame
from wordle_api import GameStatus
from wordle_ai import WordleAI
# from wordle_db import words
from wordle_db3 import wordset
import heapq

def main():
  game = WordleGame(wordset)
  game.start_game(input("Answer (press enter for random answer): "))
  ai = WordleAI(wordset)

  while True:
    print(game)
    print("Calculating...")

    top_words = []
    for word in ai.possible_words:
      heapq.heappush(top_words, (ai.calculate_entropy(word), word))
    
    for entropy, word in heapq.nlargest(10, top_words):
      print(f"{word}: {entropy}")

    if game.guess(input("Guess: ")) != GameStatus.ONGOING:
      break
    
    ai.prune_words_v2(game.get_game_state())

if __name__ == "__main__":
  main()
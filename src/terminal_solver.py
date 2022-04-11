from wordle_game import WordleGame
from wordle_api import GameStatus

def main():
  game = WordleGame()
  game.start_game(input("Answer (press enter for random answer): "))
  
  while True:
    print(game)
    if game.guess(input("Guess: ")) != GameStatus.ONGOING:
      break

if __name__ == "__main__":
  main()
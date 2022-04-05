import random
from wordle_ai import LetterState
from wordle_db import words

class WordleGame:
  def __init__(self):
    self.__init__(words)

  def __init__(self, words):
    self.words = words

  def guess_word(self, word):
    if len(self.game_state) >= 6 or "".join([guess["letter"] for guess in self.game_state[-1]]) == self.answer:
      return

    letter_indices = self.letter_indices.copy()
    guess = []
    for i, c in enumerate(word):
      if c in letter_indices:
        colour = LetterState.EMPTY
        if i in letter_indices[c]:
          letter_indices.remove(i)
          colour = LetterState.GREEN
        else:
          colour = LetterState.YELLOW
        guess.append({ "letter" : c, "state" : colour })
    self.game_state.append(guess)
    return self.game_state

  def start_game(self, answer):
    self.answer = answer
    self.game_state = []
    self.letter_indices = {}
    for i, letter in enumerate(answer):
      if letter in self.letter_indices:
        self.letter_indices[letter].add(i)
      else:
        self.letter_indices[letter] = {i}

  def start_game(self):
    self.start_game(random.choice(self.words))
  
  def get_state(self):
    return self.game_state
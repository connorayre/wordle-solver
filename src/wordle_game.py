import random
from wordle_ai import LetterState
from wordle_db import words

class WordleGame:
  def __init__(self, words = words):
    self.words = words

  def guess_word(self, word):
    if len(self.game_state) >= 6 or (len(self.game_state) > 0 and "".join([guess["letter"] for guess in self.game_state[-1]]) == self.answer):
      return

    letter_indices = self.letter_indices.copy()
    guess = []
    for i, c in enumerate(word):
      colour = LetterState.EMPTY
      if c in letter_indices:
        if i in letter_indices[c]:
          letter_indices[c].remove(i)
          colour = LetterState.GREEN
        else:
          colour = LetterState.YELLOW
      guess.append({ "letter" : c, "state" : colour })
    self.game_state.append(guess)
    return self.game_state

  def start_game(self, answer = ""):
    if answer == "": 
      self.answer = random.choice(self.words)
    else:
      self.answer = answer
    self.game_state = []
    self.letter_indices = {}
    for i, letter in enumerate(answer):
      if letter in self.letter_indices:
        self.letter_indices[letter].add(i)
      else:
        self.letter_indices[letter] = set([i])
  
  def get_state(self):
    return self.game_state
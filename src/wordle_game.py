import random
from wordle_ai import LetterState
from wordle_db import words as word_db
from wordle_api import GameStatus

class WordleGame:
  def __init__(self, words = word_db):
    self.words = words

  def guess(self, word):
    if len(word) != 5 or word not in self.words:
      return GameStatus.ONGOING

    # if len(self.game_state) >= 6:
    #   return GameStatus.MAX_GUESSES

    if len(self.game_state) > 0 and "".join([guess["letter"] for guess in self.game_state[-1]]) == self.answer:
      return GameStatus.ANSWER_FOUND

    letter_indices = {}
    for letter in self.letter_indices:
      letter_indices[letter] = set(self.letter_indices[letter])

    guess = []
    for i, c in enumerate(word):
      if c in letter_indices and i in letter_indices[c]:
        letter_indices[c].remove(i)
        colour = LetterState.GREEN
        guess.append({ "letter" : c, "state" : colour, "position": i })
      else:
        guess.append({})

    for i, c in enumerate(word):
      colour = LetterState.EMPTY
      if not guess[i]:
        if c in letter_indices and len(letter_indices[c]) > 0:
          colour = LetterState.YELLOW          
        guess[i] = { "letter" : c, "state" : colour, "position": i }
    
    self.game_state.append(guess)

    if word == self.answer:
      return GameStatus.ANSWER_FOUND

    # if len(self.game_state) >= 6:
    #   return GameStatus.MAX_GUESSES

    return GameStatus.ONGOING

  def start_game(self, answer = ""):
    if answer == "": 
      self.answer = random.choice(tuple(self.words))
    else:
      self.answer = answer

    self.game_state = []
    self.letter_indices = {}

    for i, letter in enumerate(self.answer):
      if letter in self.letter_indices:
        self.letter_indices[letter].add(i)
      else:
        self.letter_indices[letter] = set([i])

    return GameStatus.ONGOING

  def __str__(self):
    output = ""

    for guess in self.game_state:
      word = ""
      for letter in guess:
        word += letter["letter"]
        if letter["state"] == LetterState.GREEN:
          output += u"\U0001F7E9"
        elif letter["state"] == LetterState.YELLOW:
          output += u"\U0001F7E8"
        else:
          output += u"\u2B1B"

      output += f" {word}\n"
    
    return output
  
  def get_state(self):
    return self.game_state

  def get_game_state(self):
    return self.game_state[-1]
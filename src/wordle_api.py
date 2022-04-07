# ------------------------------------------------------------------------------
# wordle_api.py
#
# April 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

# Python libraries
import requests
import json
from enum import Enum
if __name__ == "src.wordle_api":
    from src.wordle_ai import LetterState
else:
    from wordle_ai import LetterState

class GameStatus(Enum):
    STARTED         = 1
    ONGOING         = 2
    MAX_GUESSES     = 3
    ANSWER_FOUND    = 4

class WordleAPI():

    def __init__(self):
        self.url = 'https://word.digitalnook.net/'
        self.game_state = []    # {'letter':char,'state':str,'position':int}
        self.guess_history = []
        self.id = None
        self.key = None
        self.num_guesses = 0
        self.answer_found = False
        self.answer = None

    
    def start_game(self):
        print("Starting game")
        # Init variables
        self.game_state = []
        self.guess_history = []
        self.num_guesses = 0
        self.answer = None
        request_url = self.url + 'api/v1/start_game/'

        # Send request
        response = requests.post(request_url)
        self._print_response(response)

        # Set response values
        response_data = json.loads(response.text)   # convert to dict
        self.id = response_data['id']
        self.key = response_data['key']

        return GameStatus.STARTED

    def guess(self, guessed_word):
        if self.num_guesses >= 6:
            print("Max guesses already performed")
            return GameStatus.MAX_GUESSES
        print(f"Submitting guess: {guessed_word}")
        self.num_guesses += 1
        guessed_word.lower()
        # Set variables
        request_url = self.url + 'api/v1/guess/'
        data = {
            'id': self.id,
            'key': self.key,
            'guess': guessed_word
        }
        self.guess_history += [guessed_word]

        # Send request
        response = requests.post(request_url, json=data)

        # Set response values
        response_data = json.loads(response.text)   # get list of data
        self._format_response(response_data)
        
        # Add to game_state
        self.game_state += response_data

        # Evaluate response for answer found
        if self._is_answer_found(response_data):
            print(f"Answer found: {guessed_word}")
            return GameStatus.ANSWER_FOUND

        # Return status
        if self.num_guesses >= 6:
            return GameStatus.MAX_GUESSES
        return GameStatus.ONGOING

    def finish_game(self):
        print("Calling finish_game()")
        print(f"Number of guesses made: {self.num_guesses}")
        # Set data
        data = {
            'id': self.id,
            'key': self.key
        }
        request_url = self.url + 'api/v1/finish_game/'

        # Send request
        response = requests.post(request_url, json=data)

        # Set response value
        response_data = json.loads(response.text)

        self.answer = response_data['answer']
        print(f"Answer: {self.answer}")

    def _print_response(self, response):
        print(f"Status code: {response.status_code}")
        print(f"Response:\n{response.json()}")

    def _is_answer_found(self, response):
        for data in response:
            if data['state'] != LetterState.GREEN:
                return False
        return True

    def _format_response(self, response):
        for i, data in enumerate(response):
            # Add position field
            data['position'] = i
            # Use enum instead of int
            data['state'] = LetterState(data['state'])

    def get_game_state(self):
        return self.game_state
    

if __name__ == "__main__":
    a = WordleAPI()
    a.start_game()
    i = 0
    result = GameStatus.STARTED
    while a.guess('crane') != GameStatus.MAX_GUESSES:
        i+= 1
        print(i)
    print(f"Num guesses made: {i}")
    #a.guess('crane')
    #a.guess('oasis')
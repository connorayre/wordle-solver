Letter State Enum
```python
Empty = 0
Yellow = 1
Green = 2
```

Game State
- array of all guesses (where guesses are an array of letter objects)
```json
[
  [
    {
      "letter": "char", 
      "state": "LetterState"
    }
  ],
]
```

Game Class
- `get_state(): GameState`
- `guess_word(word: str): GameState`
- `start_game(): GameState`
- `print_state()`

AI Class
- `remaining_words: [str]`
- `pick_word(game_state: GameState): str`
  - first guess hard coded
- `calculate_entropy(word: str, game_state: GameState): float`
- `prune_words(game_state: GameState): [str]`
- `calculate_frequency(word: str): float`

Converter Class
- `open_game()`
- `html_to_game_state(): GameState`

`python main.py --browser`

Main
1. `start_game` / `open_game`
2. `get_state` / `html_to_game_state`
3. `pick_word`
4. `guess_word` / `guess_word_in_browser`
5. `print_state`
6. repeat 2-5 until 6 guesses or correct

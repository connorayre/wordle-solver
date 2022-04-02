# ------------------------------------------------------------------------------
# wordle_ai.py
#
# March 2022, Connor Ayre, Tom Zhu, Zakaria Ismail
#
# Copyright (c) 2022
# All rights reserved.
# ------------------------------------------------------------------------------

from typing import GameState, List
class WordleAI:

    def __init__(self):
        pass

    def _get_filters(game_state: GameState):
        """
        Returns new Filter objects based on last guess
        results.

        Grey result creates Filter that removes letter 
        at all positions (0-4).
            - creates RemoveFilter (no positions arg needed)
        Yellow result creates Filter that removes letter
        at single position where it was found, but should
        keep words when letter is found at other positions
            - creates KeepFilter for multiple positions
            and RemoveFilter for single yellow position
        Green result
            - creates KeepFilter for single green position
            - Q: how to deal with multiple occurring letter 
            case?

        
        Q: Should I do some filtering for greens? YES!
        This means you should remove EVERY SINGLE OTHER
        LETTER in the alphabet at that position OR you
        could check that the letter is at the position
        Q: couldn't this be simplified by keeping a set
        of letters to remove and a set to keep? You can MAP
        letters to operation?
        Q: How do I deal with repeat letters?
        """
        pass

    def prune_words(self, game_state: GameState):
        """
        Prune words from the set of words.

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        Returns:
            -
        """
        pass

    def _get_keep_map(self, game_state) -> dict:
        """
        Gets position->list of letters MAP describing...

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        Returns:
            - 
        """
        
        pass
    
    def _get_remove_map(self, game_state) -> dict:
        """
        Gets letter->list MAP describing...

        Args:
            - game_state ('List[Dict]): list of dictionaries describing guess outcomes
        Returns:
            - 
        """
        pass


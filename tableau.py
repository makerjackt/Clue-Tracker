from assignment import Assignment
from itertools import repeat

class Tableau:
    """
    A Tableau represents all the information collected about the location of every card.
    In the Tableau's grid, each "column" represents a location a card could be:
        - Among the leftover cards revealed to everyone is  -1
        - Inside the secret envelope is 0
        - Inside a given player's hand is the corresponding player number
    Each "row" of the grid is a particular card in the game.
    The grid is accessed as grid[col_num][row_num].
    Each point on the gird has a value:
        - If that card is known to be in that location, it is 1
        - If that card is known to not be in that location, it is -1
        - If it is unknown whether the card is in that location or not, it is 0
    A row or column is solved when none of the points in it have value 0.
    The Tableau is completed when the 0 column is solved, i.e. the cards in the secret envelope are discovered
    Finally, in the condition array are conditions for the cards that could be in a players hand.
    Conditions are 2 or 3 length tuples of cards, and the statement implied by it is:
        The given player has at least one of these in their hand
    This information is collected when a player shows a card to another player after a suggestion
    When checking if a given arrangement of cards is possible, the condition array is checked.
    The array is accessed conditions[player_num][index].
    Not every player will have an equal number of conditions
    """
    def __init__(self, num_players, card_to_catagory):
        self._num_players = num_players
        self._card_to_catagory = card_to_catagory
        self._num_cards = len(card_to_catagory)
        self._num_catagories = len(set(card_to_catagory))
        self._num_cards_in_play = self._num_cards - self._num_catagories
        self._hand_size = self._num_cards_in_play // num_players
        self._num_leftover_cards = self._num_cards_in_play % num_players
        self._grid = {i:[0 for _ in range(self._num_cards)] for i in range(-1, num_players + 1)}
        self._column_states = {i:False for i in range(-1, num_players + 1)}
        self._row_states = [False for _ in range(self._num_cards)]
        self._conditions = {i:[] for i in range(1, num_players + 1)}
        self._assignment = Assignment(num_players, card_to_catagory)
    def add_entry_to_grid(self, player, card, state):
        assert state in (-1, 1), "Invalid state given to Tableau"
        if self._grid[player][card] != 0:
            assert self._grid[player][card] == state, "Contradictory entry given to Tableau"
            # In this case there is no new information
            return
        # Otherwise the current grid point is 0 so we have new information
        if state == 1:
            assert self._assignment.try_assign(card, player), f"Information given to Tableau gave player {player} too many cards"
            # If a card location is known, then all other locations cannot have that card
            for i in range(-1, self._num_players + 1):
                if i == player:
                    continue
                self._grid[i][card] = state
        else:
            pass
    def add_entries_to_grid(self, players, cards, states):
        # At least one of players, cards, states should be iterable 
        assert type(players) != int or type(cards) != int or type(states) != int, "add_entries_to_grid given not any iterables"
        if type(players) == int:
            players = repeat(players)
        if type(cards) == int:
            cards = repeat(cards)
        if type(states) == int:
            states = repeat(states)
        for p, c, s in zip(p, c, s):
            self.add_entry_to_grid(p, c, s)

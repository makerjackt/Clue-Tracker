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
    def add_entry_to_grid(self, location, card, state):
        assert state in (-1, 1), "Invalid state given to Tableau"
        if self._grid[location][card] != 0:
            assert self._grid[location][card] == state, "Contradictory entry given to Tableau"
            # In this case there is no new information
            return
        # Otherwise the current grid point is 0 so we have new information
        if state == 1:
            assert self._assignment.try_assign(card, location), f"Information given to Tableau resulted in invalid assignment"
            # If a card location is known, then all other locations cannot have that card
            self._grid[location][card] = state
            self.add_entries_to_grid([l for l in range(-1, self._num_players + 1) if l != location], card, -1)
        else:
            # if there aren't at least two spots left, then since we checked above that this is new information
            # there is only one spot left which cannot be marked as -1
            assert len(self.open_in_row(card)) >= 2, \
            f"Tableau given information that prevents card {card} from being in any location"
            if location == -1:
                assert len(self.open_in_column(location)) > self._num_leftover_cards, \
                "Tableau given information that eliminates too many cards from being leftover"
            elif location == 0:
                catagory = self._card_to_catagory[card]
                assert len([c for c in self.open_in_column(location) if self._card_to_catagory[c] == catagory]) > 1, \
                f"Tableau given information that elminates all cards in {catagory} from secret envelope"
            else:
                assert len(self.open_in_column(location)) > self._hand_size, \
                f"Tableau given information that prevents player {location} from having {self._hand_size} cards"
            self._grid[location][card] = state
    def print_grid(self):
        for c in range(self._num_cards):
            for l in range(-1, self._num_players + 1):
                s = str(self._grid[l][c])
                if len(s) == 1:
                    s = " " + s
                print(s, end = "  ")
            print()
    def open_in_column(self, location):
        # return list of cards in column that have state 0 or 1
        return [c for c in range(self._num_cards) if self._grid[location][c] >= 0]
    def open_in_row(self, card):
        # return list of location in row that have state 0 or 1
        return [l for l in range(-1, self._num_players + 1) if self._grid[l][card] >= 0]
    def add_entries_to_grid(self, locations, cards, states):
        # At least one of players, cards, states should be iterable 
        assert type(locations) != int or type(cards) != int or type(states) != int, "add_entries_to_grid not given any iterables"
        if type(locations) == int:
            locations = repeat(locations)
        if type(cards) == int:
            cards = repeat(cards)
        if type(states) == int:
            states = repeat(states)
        for l, c, s in zip(locations, cards, states):
            self.add_entry_to_grid(l, c, s)

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
            self._row_states[card] = True
            # that row is now completed
        else:
            # if there aren't at least two spots left, then since we checked above that this is new information
            # there is only one spot left which cannot be marked as -1
            assert len(self.search_row(card, (0, 1))) >= 2, \
            f"Tableau given information that prevents card {card} from being in any location"
            if location == -1:
                assert len(self.search_column(location, (0, 1))) > self._num_leftover_cards, \
                "Tableau given information that eliminates too many cards from being leftover"
            elif location == 0:
                catagory = self._card_to_catagory[card]
                assert len([c for c in self.search_column(location, (0, 1)) if self._card_to_catagory[c] == catagory]) > 1, \
                f"Tableau given information that elminates all cards in {catagory} from secret envelope"
            else:
                assert len(self.search_column(location, (0, 1))) > self._hand_size, \
                f"Tableau given information that prevents player {location} from having {self._hand_size} cards"
            self._grid[location][card] = state
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
    def check_grid(self, location, card):
        return self._grid[location][card]
    def print_grid(self):
        print(6 * " ", end = "")
        for l in range(-1, self._num_players + 1):
            s = str(self._column_states[l])
            if self._column_states[l]:
                s = " " + s
            print(s, end = "  ")
        print()
        for c in range(self._num_cards):
            s = str(self._row_states[c])
            if self._row_states[c]:
                s = " " + s
            print(s, end = "  ")
            for l in range(-1, self._num_players + 1):
                s = 3 * " " + str(self._grid[l][c])
                if self._grid[l][c] in (0, 1):
                    s = " " + s
                print(s, end = "  ")
            print()
    def search_column(self, location, condition):
        # condition int or tuple of ints
        return [c for c in range(self._num_cards) 
                if (self._grid[location][c] == condition if type(condition) == int else self._grid[location][c] in condition)]
    def search_row(self, card, condition):
        # condition int or tuple of ints
        return [l for l in range(-1, self._num_players + 1) 
                if (self._grid[l][card] == condition if type(condition) == int else self._grid[l][card] in condition)]
    def unkown_cards(self):
        return [c for c in range(self._num_cards) if not self._row_states[c]]
    def iterate_leftover(self) -> bool:
        # Returns true if new information is found
        if self._column_states[-1]:
            return False
        open_in_leftover = len(self.search_column(-1, (0, 1)))
        assert open_in_leftover >= self._num_leftover_cards, "In Tableau it is not possible to have enough leftover cards"
        if open_in_leftover == self._num_leftover_cards: 
            self._column_states[-1] = True
            for c in range(self._num_cards):
                if self._grid[-1][c] == 0:
                    self.add_entry_to_grid(-1, c, 1)
            return True
        definite_in_leftover = len(self.search_column(-1, 1))
        assert definite_in_leftover <= self._num_leftover_cards, "In Tableau too many cards have been set as leftover cards"
        if definite_in_leftover == self._num_leftover_cards:
            self._column_states[-1] = True
            for c in range(self._num_cards):
                if self._grid[-1][c] == 0:
                    self.add_entry_to_grid(-1, c, -1)
            return True
        return False
    def iterate_players(self) -> bool:
        # Returns true if new information is found
        iterated = False
        for p in range(1, self._num_players + 1):
            if self._column_states[p]:
                continue
            open_in_hand = len(self.search_column(p, (0, 1)))
            assert open_in_hand >= self._hand_size, \
            f"In Tableau it is not possible to have enough cards in player {p}'s hand"
            if open_in_hand == self._hand_size: 
                self._column_states[p] = True
                for c in range(self._num_cards):
                    if self._grid[p][c] == 0:
                        self.add_entry_to_grid(p, c, 1)
                return True
            definite_in_hand = len(self.search_column(p, 1))
            assert definite_in_hand <= self._hand_size, \
            f"In Tableau too many cards have been put in player {p}'s hand"
            if definite_in_hand == self._hand_size:
                self._column_states[p] = True
                for c in range(self._num_cards):
                    if self._grid[p][c] == 0:
                        self.add_entry_to_grid(p, c, -1)
                return True
        return False
    def iterate_secret(self) -> bool:
        if self._column_states[0]:
            return False
        all_catagories_complete = True
        iterated = False
        for catagory in range(self._num_catagories):
            cards_in_catagory = [c for c in range(self._num_cards) if self._card_to_catagory[c] == catagory]
            catagory_incomplete = len([c for c in self.search_column(0, 0) if c in cards_in_catagory]) > 0
            all_catagories_complete = all_catagories_complete and not catagory_incomplete
            if catagory_incomplete:
                # if this succeeds, the catagory is incomplete
                open_in_catagory = len([c for c in self.search_column(0, (0, 1)) if c in cards_in_catagory])
                assert open_in_catagory >= 1, f"In Tableau secret envelope cannot have a card of catagory {catagory}"
                if open_in_catagory == 1:
                    for c in cards_in_catagory:
                        if self._grid[0][c] == 0:
                            self.add_entry_to_grid(0, c, 1)
                    iterated = True
                    continue
                definite_in_catagory = len([c for c in self.search_column(0, 1) if c in cards_in_catagory])
                assert definite_in_catagory <= 1, \
                f"In Tableau secret envelope has more than one a card of catagory {catagory}"
                if definite_in_catagory == 1:
                    for c in cards_in_catagory:
                        if self._grid[0][c] == 0:
                            self.add_entry_to_grid(0, c, -1)
                    iterated = True
        self._column_states[0] = all_catagories_complete # only true after iteration if all catagories are complete
        return iterated
    def iterate_cards(self) -> bool:
        pass
    def satisfy_players(self) -> bool:
        for p in range(1, self._num_players + 1):
            if len(self._conditions[p]) == 0:
                # if there are no conditions, any assignment is valid
                continue
            unkown_cards = self.unkown_cards()
    def satisfy_collective(self) -> bool:
        pass
    def update(self):
        # update is how the Tableau deduces new information about the location of the cards.
        # It loops through each deduction step, and if new information is discovered
        # then the loop restarts. If all the deduction steps are completed and no new
        # information is discovered, then the loop is exited.
        while True:
            # do basic checks on the leftover cards column
            if self.iterate_leftover():
                continue
            # do basic checks on the secret cards column
            if self.iterate_secret():
                continue
            # do basic checks on each player column
            if self.iterate_players():
                continue
            # check each card to see if the possible locations it can be have dropped to 1
            if self.iterate_cards():
                continue
            # checks conditions on each individual players hand to see if any information can be found
            # e.g. A player must have a certain card in their hand, or they must not have a certain card
            if self.satisfy_players():
                continue
            # checks conditions on all players together to see if any information can be found
            # e.g. A certain player must have a certain card in their hand, or
            # a certain player must not have a certain card in their hand
            if self.satisfy_collective():
                continue
            break


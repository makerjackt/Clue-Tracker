class Assignment:
    """
    Assignments represent a partial or complete way of assigning cards in the game.
    Each card is assigned to:
                             a player (indicated by player number),
                             the leftover cards (indicated by -1),
                             the secret envelope (indicated by 0),
                             or is left unassigned
    Every assignment is valid:
                              each player is assigned no more cards than they can have in their hand
                              the secret envelope has at most one card of each catagory
                              the leftover cards are always assigned if there are any
    """
    def __init__(self, num_players, card_to_catagory):
        self._num_players = num_players
        self._card_to_catagory = card_to_catagory
        self._num_cards = len(card_to_catagory)
        self._num_catagories = len(set(card_to_catagory))
        self._num_cards_in_play = self._num_cards - self._num_catagories
        self._hand_size = self._num_cards_in_play // num_players
        self._num_leftover_cards = self._num_cards_in_play % num_players
        self._card_to_assignment = [None for _ in range(self._num_cards)]
    def try_assign(self, card: int, assignment: int):
        # Try to assign card a given assignment, return True is successful, False otherwise
        assert card >= 0 and card < self._num_cards, "Invalid card index given"
        assert assignment >= -1 and assignment <= self._num_players, "Invalid assignment type given"
        # Based on what assignment is given, different checks must be performed
        if assignment == -1:
            # No more than self._num_leftover_cards can be assigned as leftover cards
            if len([None for a in self._card_to_assignment if a == -1]) == self._num_leftover_cards:
                return False
        elif assignment == 0:
            # A card can't be assigned to the secret envelope if a card with the same catagory 
            # is already assigned there
            for c, a in enumerate(self._card_to_assignment):
                if a == 0 and self._card_to_catagory[card] == self._card_to_catagory[c]:
                    return False
        else:
            # No more than self._hand_size cards can be assigned a players hand
            if len([None for a in self._card_to_assignment if a == assignment]) == self._hand_size:
                return False
        self._card_to_assignment[card] = assignment
        return True
    def deassign(self, card: int):
        # Deassign the given card from its assignment, this always perserves validity
        # because the limits are all upper bounds.
        assert card >= 0 and card < self._num_cards, "Invalid card index given"
        self._card_to_assignment[card] = None
    def cards_with_assignment(self, assignment: int):
        # Return list of all cards with a given assignment
        assert assignment >= -1 and assignment <= self._num_players, "Invalid assignment type given"
        return [c for c, a in enumerate(self._card_to_assignment) if a == assignment]
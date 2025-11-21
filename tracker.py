from itertools import chain
from utils import input_unsigned_int

num_players = input_unsigned_int("How many players?: ", lb=3, ub=7, err="Please input a number from 3 to 6")

user_player = input_unsigned_int("What player number are you (player 1 takes the first turn, then player 2 takes the second turn, etc.)?: ",
                                 lb=1, ub=num_players + 1, err=f"Please input a number from 1 to {num_players}")

characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
locations = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Library", "Study"]

num_cards_in_play = len(characters) + len(weapons) + len(locations) - 3
num_cards_per_hand = num_cards_in_play // num_players
num_leftover_cards = num_cards_in_play % num_players

print("The following numbering convention is used:")
for i, name in enumerate(chain(characters, weapons, locations)):
    print(f"{i}\t=\t{name}")

leftover_cards = []
if num_leftover_cards > 0:
    print("Please input the leftover cards that were revealed to everyone, one at a time below:")
    for i in range(num_leftover_cards):
        card = None
        while card == None:
            card = input_unsigned_int(f"Input leftover card numer {i + 1}: ", lb=0, ub=num_cards_in_play, 
                                      err=f"Please input a number from 0 to {num_cards_in_play - 1}")
            if card in leftover_cards:
                print("That leftover card has already been input. Please input the next one.")
                card = None
        leftover_cards.append(card)

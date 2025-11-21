digits = set("0123456789")

num_players = 0
while num_players < 3 or num_players > 6:
    user_input = input("How many players?: ")
    if len(user_input) == 1 and user_input in digits:
        num_players = int(user_input)
    if num_players < 3 or num_players > 6:
        print("Please input a number from 3 to 6")

user_player = 0
while user_player < 1 or user_player > num_players:
    user_input = input("What player number are you (player 1 takes the first turn, then player 2 takes the second turn, etc.)?: ")
    if len(user_input) == 1 and user_input in digits:
        user_player = int(user_input)
    if user_player < 1 or user_player > num_players:
        print(f"Please input a number from 1 to {num_players}")

characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
locations = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Library", "Study"]
digits = set("0123456789")

num_players = 0
while num_players < 3 or num_players > 6:
    user_input = input("How many players?: ")
    if len(user_input) == 1 and user_input in digits:
        num_players = int(user_input)
    if num_players < 3 or num_players > 6:
        print("Please input a number from 3 to 6")

characters = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
locations = ["Ballroom", "Billiard Room", "Conservatory", "Dining Room", "Hall", "Kitchen", "Lounge", "Library", "Study"]
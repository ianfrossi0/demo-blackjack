class Player:
    def __init__(self, name, initial_amount):
        self.name = name
        self.score = initial_amount
        self.can_play = True  # If player's points are below entry bet, they cannot play

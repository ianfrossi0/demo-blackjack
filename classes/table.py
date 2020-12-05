import random
import re
from .card import Card
from .hand import Hand


class Table:
    def __init__(self, players):
        self.ICONS = ["Hearts", "Tiles", "Clovers", "Pikes"]
        self.played_cards = {"Hearts": set(), "Tiles": set(), "Clovers": set(), "Pikes": set()}
        self.player_hands = {}
        self.players = players
        
        # Initialize player hands
        for i in range(int(players)):
            self.player_hands[i+1] = Hand()
            first_card = self.getNewCard()
            second_card = self.getNewCard()
            self.player_hands[i+1].addCard(first_card)
            self.player_hands[i+1].addCard(second_card)

            if (first_card.number == 1 and second_card.number == 10) or\
                    (first_card.number == 10 and second_card.number == 1):
                self.player_hands[i+1].natural = True
    
    # Generate a new random card
    def getNewCard(self) -> object:
        # Generate random card
        new_card = Card(random.randint(1, 13), self.ICONS[random.randint(0, 3)])
        
        # Keep generating new cards if they have already
        # been withdrawn from the deck
        while new_card.number in self.played_cards[new_card.icon]:
            new_card = Card(random.randint(1, 13), self.ICONS[random.randint(0, 3)])
        
        # Add card to withdrawn stack
        self.played_cards[new_card.icon].add(new_card.number)
        
        return new_card
    
    # Show hand of player as string
    def showHand(self, player):
        for card in self.player_hands[player].cards:
            print(card.getString())
    
    # This method will be called from main to interact
    # with a player hand from playerHands dict
    def addCard(self, player):
        self.player_hands[player].addCard(self.getNewCard())
    
    # Calculate player score based on cards on hand
    def getPlayerScore(self, player) -> int:
        return self.player_hands[player].getScore()
    
    # Calculate player soft score assuming all aces are soft 11
    def getPlayerSoftScore(self, player) -> int:
        return self.player_hands[player].getSoftScore()
    
    # Check if played has decided to stand his hand
    def isPlayerStanding(self, player) -> bool:
        return self.player_hands[player].stand
    
    # Player has decided to stay. Set stand to True
    def playerStand(self, player):
        self.player_hands[player].stand = True
    
    # Check whether all players have decided to
    # stay or are busted
    def haveAllPlayersStoodOrBusted(self) -> bool:
        for hand in self.player_hands.values():
            if not hand.stand and not hand.busted:
                return False
        return True
    
    # Check whether played is busted
    def isPlayerBusted(self, player) -> bool:
        if self.getPlayerScore(player) > 21:
            self.player_hands[player].busted = True
        return self.player_hands[player].busted
    
    # Ask to player if their aces are soft
    def assignValueToAces(self, player):
        if self.player_hands[player].contains_ace:
            for card in self.player_hands[player].cards:
                if card.isAce():
                    print(f"You have an {card.getString()}. ", end='')
                    while not re.match('[1]{1,2}', value := input(f"Do you want to use it with as a 1 or as an 11?\n")):
                        print("\nEnter a valid option \n\n")
                    if value == '11':
                        card.soft = True
                    print("\n")

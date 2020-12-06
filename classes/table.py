import random
import re
from .card import Card
from .hand import Hand
from .dealer import Dealer

# TODO: since players start at index 1, maybe refactor code  \
#  to allow the dealer to exist at index 0? (may simplify on the long run)


class Table:
    def __init__(self, players):
        self.ICONS = ["Hearts", "Tiles", "Clovers", "Pikes"]
        self.played_cards = {"Hearts": set(), "Tiles": set(), "Clovers": set(), "Pikes": set()}
        self.player_hands = {}
        self.players = players
        self.dealer = Dealer()
        dealer_may_have_natural = False
        
        # Initialize player hands
        for i in range(int(players)):
            self.player_hands[i+1] = Hand()

        # Deal initial cards. This for will loop ( players + 1 ) * 2 times,
        # as it will give one card at a time to each player AND the dealer
        for i in range((int(players)+1)*2):
            current_card = self.getNewCard()

            # It's the dealer's turn to receive a card
            if (i+1) % (int(players)+1) == 0:
                if i+1 > int(players)+1:
                    # Second card must be dealt facing down
                    current_card.visible = False
                elif current_card.number == 10 or current_card.isAce():
                    # If the dealer deals a 10 or an ace as his face up card
                    # they need to check whether they have a natural or not
                    dealer_may_have_natural = True
                self.dealer.addCard(current_card)
            else:
                if i+1 > int(players):
                    self.player_hands[i-int(players)].addCard(current_card)
                else:
                    self.player_hands[i+1].addCard(current_card)

        for i in range(int(players)):
            self.player_hands[i+1].natural = self.checkPlayerNatural(i+1)

        if dealer_may_have_natural:
            self.dealer.hand.natural = self.checkDealerNatural()
    
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

    # Show hand of dealer as string
    def showDealerHand(self):
        for card in self.dealer.hand.cards:
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

    # Return score taking into consideration that the dealer may have to stand on a soft ace
    def getDealerScore(self) -> int:
        return self.dealer.hand.getSoftScore() if self.dealer.has_to_soft else self.dealer.hand.getSoftScore()
    
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

    # Check if the dealer must keep picking up cards
    def hasDealerStoodOrBusted(self) -> bool:
        self.dealer.checkForStandOrBust()
        if self.dealer.hand.stand or self.dealer.hand.busted:
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

    # Check if player has a natural hand on deal
    def checkPlayerNatural(self, player) -> bool:
        return True if (self.player_hands[player].cards[0].isAce() and
                        self.player_hands[player].cards[0].number == 10) or \
                       (self.player_hands[player].cards[0].number == 10 and
                        self.player_hands[player].cards[0].isAce()) else False

    # Check if dealer has a natural hand on deal
    def checkDealerNatural(self) -> bool:
        return True if (self.dealer.cards[0].isAce() and
                        self.dealer.cards[0].number == 10) or \
                       (self.dealer.cards[0].number == 10 and
                        self.dealer.cards[0].isAce()) else False

    # Does any player have a natural?
    def anyPlayerHasNatural(self) -> bool:
        for i in range(int(self.players)):
            if self.checkPlayerNatural(i+1):
                return True
        return False

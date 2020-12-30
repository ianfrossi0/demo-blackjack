import random
import re
from operator import itemgetter
from .player import Player
from .card import Card
from .hand import Hand
from .dealer import Dealer
from .constants import *


class Table:
    def __init__(self, players):
        self.played_cards = {"Hearts": set(), "Tiles": set(), "Clovers": set(), "Pikes": set()}
        self.player_hands = []
        self.bets = dict()  # TODO
        self.players = players
        self.dealer = Dealer()
        self.dealer_may_have_natural = False
        self.turn = 1

        # Initialize players and their hands and add tuple to player_hands list
        for i in range(self.players):
            self.player_hands.append((Player(input(f"\tEnter name for player {i+1}: "), 1500), Hand()))

    # Deal card to player or dealer depending on player parameter
    def deal(self, player):
        current_card = self.get_new_card()

        if current_card is not None:
            if player != -1:
                self.player_hands[player][1].add_card(current_card)

                if len(self.player_hands[player][1].cards) == 2:
                    self.player_hands[player][1].natural = self.check_player_natural(player)
            else:  # It's the dealer's turn to receive a card
                if len(self.dealer.hand.cards) == 1:  # Second card must be dealt facing down
                    current_card.visible = False
                elif len(self.dealer.hand.cards) == 0 and \
                        (current_card.number == 10 or current_card.is_ace()):
                    # If the dealer deals a 10 or an ace as his face up card
                    # they need to check whether they have a natural or not
                    self.dealer_may_have_natural = True
                self.dealer.add_card(current_card)

                if self.dealer_may_have_natural:
                    self.dealer.hand.natural = self.check_dealer_natural()

        return current_card

    # Check whether all players and dealer have received their initial deal
    def finished_dealing(self) -> bool:
        for p in self.player_hands:
            if len(p[1].cards) < 2:
                return False
        return len(self.dealer.hand.cards) >= 2

    # Check whether player still needs cards
    def up_for_initial_deal(self, player) -> bool:
        return True if self.get_card_count(player) < 2 else False

    # Return card count of player or dealer
    def get_card_count(self, player) -> int:
        if player != -1:  # Check player
            return self.player_hands[player][1].get_card_count()
        else:  # Check dealer
            return self.dealer.hand.get_card_count() - 1

    # Generate a new random card
    def get_new_card(self) -> object:
        if len(self.played_cards['Pikes']) + len(self.played_cards['Hearts']) + \
                len(self.played_cards['Tiles']) + len(self.played_cards['Clovers']) == 51:
            return None  # No more cards available in deck!

        # Generate random card
        new_card = Card(random.randint(1, 13), ICONS[random.randint(0, 3)])

        # Keep generating new cards if they have already
        # been withdrawn from the deck
        while new_card.number in self.played_cards[new_card.icon]:
            new_card = Card(random.randint(1, 13), ICONS[random.randint(0, 3)])

        # Add card to withdrawn stack
        self.played_cards[new_card.icon].add(new_card.number)
        
        return new_card
    
    # Calculate player score based on cards on hand
    def get_player_score(self, player) -> int:
        if player != -1:
            return self.player_hands[player][1].get_score()
        else:
            # Return score taking into consideration that the dealer may have to stand on a soft ace
            return self.dealer.hand.get_soft_score() if self.dealer.has_to_soft else self.dealer.hand.get_soft_score()

    # Calculate player soft score assuming all aces are soft 11
    def get_player_soft_score(self, player) -> int:
        return self.player_hands[player][1].get_soft_score()
    
    # Check if played has decided to stand his hand
    def is_player_standing(self, player) -> bool:
        if player != -1:
            return self.player_hands[player][1].stand
        else:
            self.dealer.check_for_stand_or_bust()
            return self.dealer.hand.stand

    # Player has decided to stay. Set stand to True
    def player_stand(self, player):
        if player != -1:
            self.player_hands[player][1].stand = True
        else:
            self.dealer.hand.stand = True

    # Check whether all players have decided to stay or are busted
    def have_all_players_stood_or_busted(self) -> bool:
        # Check if a player is still playing
        for i in range(self.players):
            if not self.player_hands[i][1].stand and not self.player_hands[i][1].busted:
                return False

        # Check if dealer is still playing
        self.dealer.check_for_stand_or_bust()
        if not self.dealer.hand.stand and not self.dealer.hand.stand:
            return False

        return True  # No one is playing
    
    # Check whether played is busted
    def is_player_busted(self, player) -> bool:
        if player != -1:
            if self.get_player_score(player) > 21:
                self.player_hands[player][1].busted = True
            return self.player_hands[player][1].busted
        else:
            self.dealer.check_for_stand_or_bust()
            return self.dealer.hand.busted

    # Ask to player if their aces are soft
    def assign_value_to_aces(self, player):
        if self.player_hands[player][1].contains_ace:
            for card in self.player_hands[player][1].cards:
                if card.is_ace():
                    print(f"You have an {card.get_string()}. ", end='')
                    while not re.match('[1]{1,2}', value := input(f"Do you want to use it with as a 1 or as an 11?")):
                        print("\nEnter a valid option \n")
                    if value == '11':
                        card.soft = True

    # Check if player has a natural hand on deal
    def check_player_natural(self, player) -> bool:
        return True if (self.player_hands[player][1].cards[0].is_ace() and
                        self.player_hands[player][1].cards[0].number == 10) or \
                       (self.player_hands[player][1].cards[0].number == 10 and
                        self.player_hands[player][1].cards[0].is_ace()) else False

    # Check if dealer has a natural hand on deal
    def check_dealer_natural(self) -> bool:
        return True if (self.dealer.hand.cards[0].is_ace() and
                        self.dealer.hand.cards[0].number == 10) or \
                       (self.dealer.hand.cards[0].number == 10 and
                        self.dealer.hand.cards[0].is_ace()) else False

    # Does any player have a natural?
    def any_player_has_natural(self) -> bool:
        for i in range(self.players):
            if self.check_player_natural(i):
                return True
        return False

    # Order player hands by score descending
    def order_hands(self) -> list:
        ordered_hands = []
        for i in range(self.players):
            if not self.player_hands[i][1].busted:
                ordered_hands.append((i, self.get_player_score(i)))
            else:
                print(f"\nPlayer {i+1} is busted! Skipping to next player...\n")
        ordered_hands.sort(key=itemgetter(1), reverse=True)
        return ordered_hands

    # Return player name
    def get_player_name(self, player):
        return self.player_hands[player][0].name

    # Checks which players have a tied score and returns index of last tied player
    @staticmethod
    def check_tie(scores):
        last_tied = 0
        while scores[last_tied] == scores[last_tied + 1] and last_tied < len(scores) - 1:
            last_tied += 1
        return last_tied

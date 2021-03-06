import random
import re
from .player import Player
from .card import Card
from .hand import Hand
from .dealer import Dealer
from .constants import *


class Table:
    def __init__(self, players):
        self.played_cards = {"Hearts": set(), "Tiles": set(), "Clovers": set(), "Pikes": set()}
        self.player_hands = []
        self.bets = dict()
        self.players = players
        self.dealer = Dealer()
        self.dealer_may_have_natural = False
        self.turn = 1

        # Initialize players and their hands and add tuple to player_hands list
        for i in range(self.players):
            self.player_hands.append((Player(input(f"\tEnter name for player {i+1}: "), 1600), Hand()))

    # Deal card to player or dealer depending on player parameter
    def deal(self, player):
        current_card = self.get_new_card()

        if current_card is not None:
            if player != -1:
                self.player_hands[player][1].add_card(current_card)

                if len(self.player_hands[player][1].cards) == 2:
                    self.player_hands[player][1].natural = self.check_player_natural(player)

                    if self.player_hands[player][1].natural:
                        print(f"[AUTO] Player has a blackjack, they stand!")
                        self.player_hands[player][1].stand = True
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
        i = 0
        for p in self.player_hands:
            if len(p[1].cards) < 2 and self.can_player_play(i):
                return False
            i += 1
        return len(self.dealer.hand.cards) >= 2

    # Check whether player still needs cards
    def up_for_initial_deal(self, player) -> bool:
        if player != -1:
            return True if self.get_card_count(player) < 2 and self.player_hands[player][0].can_play else False
        else:
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
            if not self.player_hands[i][1].stand \
                    and not self.player_hands[i][1].busted and self.can_player_play(i):
                return False

        # Check if dealer is still playing
        self.dealer.check_for_stand_or_bust()
        if not self.dealer.check_for_stand_or_bust():
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

    # Get exact amount of aces
    def get_amount_of_aces(self, player):
        aces = 0
        for card in self.player_hands[player][1].cards:
            if card.is_ace():
                aces += 1
        return aces

    # Assign real value to player ace
    def assign_value_to_aces(self, player, hard, ace_number):
        for card in self.player_hands[player][1].cards:
            if card.is_ace and ace_number == 1:
                if not hard:
                    card.soft = True
                    break
            elif card.is_ace and ace_number > 1:
                ace_number -= 1

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

    # Return player name
    def get_player_name(self, player):
        return self.player_hands[player][0].name

    # Return whether player can play or not
    def can_player_play(self, player):
        return self.player_hands[player][0].can_play

    # Check whether player can play and if possible add their bet to the list
    def initialize_player_bet(self, player):
        if self.player_hands[player][0].score >= ENTRY_BET:
            # Player has enough score to play a new hand
            self.player_hands[player][0].score -= ENTRY_BET
            self.bets[player] = ENTRY_BET
        else:
            # Player does not have enough score to play a new hand
            self.player_hands[player][0].can_play = False
        return self.can_player_play(player)

    # Check whether player wins or loses
    def check_player_win(self, player):
        # Get dealer's score once so that I don't have to get it multiple times
        dealer_score = self.get_player_score(-1)
        player_score = self.get_player_score(player)
        print(f"\n[AUTO] Dealer's score: {dealer_score}")
        print(f"[AUTO] {self.get_player_name(player)}'s score: {player_score}")

        if not self.is_player_busted(-1):
            # Dealer is not busted, check who won against them
            if self.dealer.hand.natural:
                # Dealer has a blackjack, all players that do not lose
                if player_score == dealer_score:
                    # Player also has a blackjack, tie. No changes to score.
                    print(f"[AUTO] Player {player + 1} ties a blackjack with the dealer")
                else:
                    # Player doesn't have a blackjack, loses. Score minus bet on this hand.
                    print(f"[AUTO] Player {player + 1} loses as they don't have a blackjack and the dealer does")
                    self.player_hands[player][0].score = \
                        self.player_hands[player][0].score - self.bets[player]
            else:
                if not self.player_hands[player][1].busted:
                    if not self.player_hands[player][1].natural:
                        # Player is not busted and doesn't have a blackjack.
                        # They have to check if they won against the dealer
                        if player_score < dealer_score:
                            # Hand score is lower than dealer's hand, played loses.
                            # Score minus bet on this hand.
                            print(f"[AUTO] Player {player + 1} loses as their score is lower than the dealer's")
                            self.player_hands[player][0].score = \
                                self.player_hands[player][0].score - self.bets[player]
                        elif player_score == dealer_score:
                            # Hand score is tied to the dealer's, player receives his bet back.
                            # No changes to score.
                            print(f"[AUTO] Player {player + 1} ties their score with the dealer's")
                        else:
                            # Hand score is higher than the dealer's hand, player wins.
                            # Score plus bet on this hand.
                            print(f"[AUTO] Player {player + 1} wins as their score is higher than the dealer's")
                            self.player_hands[player][0].score = \
                                self.player_hands[player][0].score + self.bets[player]
                    else:
                        # Player has a blackjack and dealer does not, win 3:2. Score times 1.5.
                        print(f"[AUTO] Player {player + 1} wins 3:2 as they have a blackjack when the dealer doesn't")
                        self.player_hands[player][0].score = \
                            self.player_hands[player][0].score + (
                                    self.bets[player] * 1.5)
                else:
                    # Player is busted and loses. Score minus bet on this hand.
                    print(f"[AUTO] Player {player + 1} loses as they are busted")
                    self.player_hands[player][0].score = \
                        self.player_hands[player][0].score - self.bets[player]
        else:
            # Dealer is busted, all players who are not win
            if not self.player_hands[player][1].busted:
                # Player is not busted, they win. Score plus bet on this hand.
                print(f"[AUTO] Player {player + 1} wins as the dealer is busted and they're not")
                self.player_hands[player][0].score = \
                    self.player_hands[player][0].score + self.bets[player]
            else:
                # Player is busted, they lose. Score minus bet on this hand.
                print(f"[AUTO] Player {player + 1} loses as both the dealer and them are busted")
                self.player_hands[player][0].score = \
                    self.player_hands[player][0].score - self.bets[player]

from .hand import Hand


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.has_to_soft = False

    def addCard(self, card):
        self.hand.addCard(card)

    def checkForStandOrBust(self):
        soft_score = self.hand.getSoftScore()
        score = self.hand.getScore()

        if not self.hand.natural:
            # Check if dealer has an ace
            if soft_score != score:
                # If using the ace as an 11 keeps the dealer's score
                # between 17 and 21 then it must be used that way
                if 17 <= soft_score <= 21:
                    self.has_to_soft = True
                    self.hand.stand = True
            elif 17 <= score <= 21:
                # If dealer's score is between 17 and 21 they must stand
                self.hand.stand = True
            elif score > 21:
                # Dealer is busted!
                self.hand.busted = True
        else:
            # Dealer has a natural (ace used as 11 and a 10), must stand
            self.has_to_soft = True
            self.hand.stand = True

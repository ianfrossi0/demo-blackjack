class Hand:
    # This init serves no other purpose than to generate
    # new instances of Hand. Must remember to do this!
    def __init__(self):
        self.cards = []
        self.stand = False
        self.busted = False
        self.natural = False

    def clear(self):
        self.cards.clear()

    # Add a card to this hand
    def add_card(self, card):
        self.cards.append(card)

    # Return how many cards this hand has
    def get_card_count(self):
        return len(self.cards)
    
    # Return sum of card numbers
    def get_score(self) -> int:
        score = 0
        for card in self.cards:
            score += card.number
            
            # Card is a soft 11, add remaining score
            if card.number == 1 and card.soft:
                score += 10
        return score
    
    # Return sum of card numbers (aces are valued 11)
    def get_soft_score(self) -> int:
        # Since using two aces as a soft ace results in
        # a score of 22, only the first ace is used as a
        # soft card, the rest are used as hard aces, valuing 1
        score = 0
        use_as_soft_ace = True
        for card in self.cards:            
            if card.is_ace() and use_as_soft_ace:
                score += 11
                use_as_soft_ace = False
            else:
                score += card.number
        return score

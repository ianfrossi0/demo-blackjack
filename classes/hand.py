class Hand:
    # This init serves no other purpose than to generate
    # new instances of Hand. Must remember to do this!
    def __init__(self):
        self.cards = []
        self.stand = False
        self.busted = False
        self.contains_ace = False
        self.natural = False
    
    # Add a card to this hand
    def addCard(self, card):
        if card.number == 1:
            self.contains_ace = True
        self.cards.append(card)
    
    # Return sum of card numbers
    def getScore(self) -> int:
        score = 0
        for card in self.cards:
            score += card.number
            
            # Card is a soft 11, add remaining score
            if card.number == 1 and card.soft:
                score += 10
        return score
    
    # Return sum of card numbers (aces are valued 11)
    def getSoftScore(self) -> int:
        score = 0
        for card in self.cards:            
            if card.number == 1:
                score += 11
            else:
                score += card.number
        return score

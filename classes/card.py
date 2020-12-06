class Card:
    def __init__(self, number, icon):
        self.number = number
        self.icon = icon
        self.visible = True
        
        # Soft refers to value for an ace
        # A soft ace is valued 11, a hard ace is valued 1
        self.soft = False
    
    # Returns whether this card is an ace or not
    def isAce(self) -> bool:
        return True if self.number == 1 else False
    
    # Return card name as string
    def getString(self):
        if self.visible:
            if self.number == 1:
                strval = "Ace"
            elif self.number == 2:
                strval = "Two"
            elif self.number == 3:
                strval = "Three"
            elif self.number == 4:
                strval = "Four"
            elif self.number == 5:
                strval = "Five"
            elif self.number == 6:
                strval = "Six"
            elif self.number == 7:
                strval = "Seven"
            elif self.number == 8:
                strval = "Eight"
            elif self.number == 9:
                strval = "Nine"
            elif self.number == 10:
                strval = "Ten"
            elif self.number == 11:
                strval = "Jack"
            elif self.number == 12:
                strval = "Queen"
            else:
                strval = "King"

            return strval + " of " + self.icon
        else:
            return "Card facing down"

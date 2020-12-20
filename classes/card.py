class Card:
    def __init__(self, number, icon):
        self.number = number
        self.icon = icon
        self.visible = True
        
        # Soft refers to value for an ace
        # A soft ace is valued 11, a hard ace is valued 1
        self.soft = False
    
    # Returns whether this card is an ace or not
    def is_ace(self) -> bool:
        return True if self.number == 1 else False
    
    # Return card name as string
    def get_string(self):
        if self.visible:
            if self.number == 1:
                str_val = "ace"
            elif self.number == 2:
                str_val = "two"
            elif self.number == 3:
                str_val = "three"
            elif self.number == 4:
                str_val = "four"
            elif self.number == 5:
                str_val = "five"
            elif self.number == 6:
                str_val = "six"
            elif self.number == 7:
                str_val = "seven"
            elif self.number == 8:
                str_val = "eight"
            elif self.number == 9:
                str_val = "nine"
            elif self.number == 10:
                str_val = "ten"
            elif self.number == 11:
                str_val = "jack"
            elif self.number == 12:
                str_val = "queen"
            else:
                str_val = "king"

            return str_val + "_of_" + self.icon
        else:
            return "card_facing_down"

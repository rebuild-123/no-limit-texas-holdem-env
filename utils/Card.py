from .hyperparameters import suit_dict, number_dict

class Card:
    def __init__(self,suit:int, number:int):
        self.suit = suit
        self.number = number
        self.suit_str = suit_dict[suit]
        self.number_str = number_dict[number]
    
    def __repr__(self):
        return 'Card(suit=%-7s, number=%-2s)'%(self.suit_str,self.number_str)
    
    def __str__(self):
        return 'Card(suit=%-7s, number=%-2s)'%(self.suit_str,self.number_str)
    
    def __lt__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The compared instance should be \"Card\"!")
        return self.number < value.number
        
    def __eq__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The compared instance should be \"Card\"!")
        return self.number == value.number and self.suit == value.suit
    
    def __ge__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The compared instance should be \"Card\"!")
        return self.number >= value.number
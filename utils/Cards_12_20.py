from random import shuffle
suit_dict = {-1:'NA',0:'spade',1:'heart',2:'diamond',3:'club'}
number_dict = {-1:'NA',0:'2',1:'3',2:'4',3:'5',4:'6',5:'7',6:'8',7:'9',8:'10',9:'J',10:'Q',11:'K',12:'A'}

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

class Cards:
    def __init__(self,cards):
        self.cards = cards
        
    def withdraw_cards(self,number):
        if len(self.cards) < number: raise ValueError('There is no enough cards!')
        temp = self.cards[:number]
        self.cards = self.cards[number:]
        return Cards(temp)
    
    def sort(self):
        self.cards = sorted(self.cards,key=lambda card: [-card.number,card.suit])
        return self
    
    def __len__(self):
        return len(self.cards)
    
    def __setitem__(self,idx,value):
        self.cards[idx] = value
    
    def __getitem__(self,idx):
        return self.cards[idx]
    
    def __repr__(self):
        return '\n'.join(['%s'%(card) for card in self.cards])
    
    def __str__(self):
        return '\n'.join(['%s'%(card) for card in self.cards])
    
    def __add__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The added instance should be \"Cards\"!")
        return Cards(self.cards+value.cards)
    
    def __radd__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The added instance should be \"Cards\"!")
        return Cards(self.cards+value.cards)
    
    def __iadd__(self,value):
        if not isinstance(value,type(self)): raise ValueError("The added instance should be \"Cards\"!")
        return Cards(self.cards+value.cards)
        
    
class Deck:
    def __init__(self):
        self.cards = Cards([Card(*divmod(i,13)) for i in range(52)])
        shuffle(self.cards)
    def reset(self):
        self.cards = Cards([Card(*divmod(i,13)) for i in range(52)])
        shuffle(self.cards)
    def withdraw_cards(self,number):
        return self.cards.withdraw_cards(number)
    def __repr__(self):
        return '\n'.join(['%s'%(card) for card in self.cards])
    def __str__(self):
        return '\n'.join(['%s'%(card) for card in self.cards])
    def __len__(self):
        return len(self.cards)
    def __getitem__(self,idx):
        return self.cards[idx]
    def __setitem__(self,idx,value):
        self.cards[idx] = value
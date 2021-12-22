from random import shuffle
from .Card import Card
from .Cards import Cards

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
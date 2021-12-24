from .Check_Rank import straight_flush,straight_flush_from_A_to_five,four_of_a_kind,\
full_house,flush,straight,straight_from_A_to_five,three_of_a_kind,two_pairs,pair,highcard

class Cards:
    def __init__(self,cards):
        self.cards = cards
        self.info = {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}  
        
    def withdraw_cards(self,number):
        if len(self.cards) < number: raise ValueError('There is no enough cards!')
        temp = self.cards[:number]
        self.cards = self.cards[number:]
        return Cards(temp)
    
    def sort(self):
        self.cards = sorted(self.cards,key=lambda card: [-card.number,card.suit])
        return self
    
    def best_combination(self):
        self.info = {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}  
        if len(self.cards) < 5: raise ValueError('the function needs at least five cards.')
        if self.info['check'] != True: self.info = straight_flush(self.cards)
        if self.info['check'] != True: self.info = straight_flush_from_A_to_five(self.cards)
        if self.info['check'] != True: self.info = four_of_a_kind(self.cards)
        if self.info['check'] != True: self.info = full_house(self.cards)
        if self.info['check'] != True: self.info = flush(self.cards)
        if self.info['check'] != True: self.info = straight(self.cards)
        if self.info['check'] != True: self.info = straight_from_A_to_five(self.cards)
        if self.info['check'] != True: self.info = three_of_a_kind(self.cards)
        if self.info['check'] != True: self.info = two_pairs(self.cards)
        if self.info['check'] != True: self.info = pair(self.cards)
        if self.info['check'] != True: self.info = highcard(self.cards)
        return self.info
    
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
from .Check_Rank import straight_flush,straight_flush_from_A_to_five,four_of_a_kind,\
full_house,flush,straight,straight_from_A_to_five,three_of_a_kind,two_pairs,pair,highcard

CHECK_LIST = (
    straight_flush,straight_flush_from_A_to_five,four_of_a_kind,
    full_house,flush,straight,straight_from_A_to_five,three_of_a_kind,two_pairs,pair,highcard
)

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
        self.info = next(
            info
            for checker in CHECK_LIST 
            if (info := checker(self.cards)) != None and info['check'] == True
        )
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
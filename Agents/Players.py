from Model import Sudo_Model
from typing import List
from utils import Card, decimal_precision
from decimal import Decimal, ROUND_HALF_DOWN

class Player:
    def __init__(self,algo:str,seat:int,money:int=1e6):
        self.algo = algo
        self.seat = seat
        self.money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.init_money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.cards = [Card(-1,-1),Card(-1,-1)]
        self.has_betted = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.has_betted_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.status = 'call'
        self.model = Sudo_Model()
    
    def reset(self):
        self.money = self.init_money
        self.cards = [Card(-1,-1),Card(-1,-1)]
        self.has_betted = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.has_betted_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.status = 'call'
        
    def reset_for_a_cycle(self):
        self.cards = [Card(-1,-1),Card(-1,-1)]
        self.has_betted = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.has_betted_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        if self.money > 0:
            self.status = 'call'
        elif self.money == 0:
            self.status = 'fold'
        elif self.money < 0:
            raise ValueError('There is something wrong!')
        
    def reset_for_a_round(self):
        self.has_betted = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        if self.status == 'fold':
            self.status = 'fold'
        elif self.money > 0:
            self.status = 'call'
        elif self.money == 0:
            self.status = 'all_in'
        elif self.money < 0:
            raise ValueError('There is something wrong!')
        
    def __str__(self):
        cards_info = ' and '.join(['%s'%(cards) for cards in self.cards])
        line_1 = f'players_{self.seat}[{self.status}] has {self.money} dollar. players_{self.seat} has betted {self.has_betted} in the round and betted {self.has_betted_in_the_cycle} in the clcye.'
        line_2 = f'players_{self.seat}[{self.status}] has {cards_info}.'
        return line_1
        
    def __repr__(self):
        cards_info = ' and '.join(['%s'%(cards) for cards in self.cards])
        line_1 = f'players_{self.seat}[{self.status}] has {self.money} dollar. players_{self.seat} has betted {self.has_betted} in the round and betted {self.has_betted_in_the_cycle} in the clcye.'
        line_2 = f'players_{self.seat}[{self.status}] has {cards_info}.'
        return line_1
    
    def calculate_bet_and_raise_(self,bet,info):
        if bet >= self.has_betted:
            raise_ = min(self.money,bet - self.has_betted)
            bet = self.has_betted + raise_
            self.money -= raise_
            self.has_betted += raise_
        elif bet < self.has_betted:
            if bet == 0:
                self.has_betted = 0
                raise_ = 0
            else:
                raise ValueError('There is something wrong')
        return bet,raise_
    
    def change_player_status(self,bet,info):
        if bet > info['bet']:
            self.status = 'raise_'
        elif self.money == 0:
            self.status = 'all_in'
        elif bet == info['bet']:
            if info['current_player'] != info['raiser']: self.status = 'call'
        elif bet < info['bet']:
            if bet == 0: 
                self.status = 'fold'
            else:
                print(bet,info['bet'])
                raise ValueError('There is something wrong!')
    
    def action(self,state,reward,info):
        if info['current_player'] == info['sb_payer'] and info['pay_bb'] == False:
            bet = info['bb']/2
        elif info['current_player'] == info['bb_payer'] and info['pay_bb'] == False:
            bet = info['bb']
        else:
            bet = self.model(state,reward,info,self.money)
        bet = Decimal(bet).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        bet,raise_ = self.calculate_bet_and_raise_(bet,info)
        self.has_betted_in_the_cycle += raise_
        
        self.change_player_status(bet,info)
        
        return {'bet':bet,'raise_':raise_}


# In[ ]:


class Players:
    def __init__(self,algos:List[str],player_number:int=6, money=1e6):
        self.algos = algos
        self.player_number = player_number
        self.money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.players = [Player(algo=algo,seat=seat,money=money) for algo,seat in zip(self.algos,range(self.player_number))]
        
    @property
    def alive_players_num(self):
        return sum((1 for player in self.players if player.money > 0 or player.has_betted != 0))
        
    def take_cards(self,cards):
        for player in self.players:
            if player.money > 0:
                player.cards = cards.withdraw_cards(2)
        
    def reset(self):
        for player in self.players:
            player.reset()
            
    def reset_for_a_cycle(self):
        for player in self.players:
            player.reset_for_a_cycle()
            
    def reset_for_a_round(self):
        for player in self.players:
            player.reset_for_a_round()
    
    def __str__(self):
        return '\n'.join(['%s'%(player) for player in self.players if player.cards != None])
    
    def __repr__(self):
        return '\n'.join(['%s'%(player) for player in self.players if player.cards != None])
    
    def __getitem__(self,idx):
        return self.players[idx]
    
    def check_raiser(self,info):
        if self.players[info['current_player']].status == 'raise_':
            for player in self.players:
                if player != self.players[info['current_player']] and player.status == 'raise_':
                    if player.money != 0:
                        player.status = 'call'
                    else:
                        player.status = 'all_in'
    
    def show(self,action,info):
        bet_or_fold = 'fold' if self.players[info['current_player']].status == 'fold' else 'bet'
        if bet_or_fold == 'fold': print('player_%d fold!'%(info['current_player']))
        elif action['bet'] > info['bet']: print('player_%d raise %f dollar!'%(info['current_player'],action['bet']))
        else: print('player_%d bet %f dollar!'%(info['current_player'],action['bet']))
        print(self)
    
    def action(self,state,reward,info):
        action = self.players[info['current_player']].action(state,reward,info)
        self.check_raiser(info)
        self.show(action,info)
        return action


from Model import Sudo_Model
from typing import List
from utils import Card, Cards, decimal_precision
from decimal import Decimal, ROUND_HALF_DOWN

class Player:
    def __init__(self,seat,money):
        self.seat = seat
        self.money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.model = Sudo_Model()
        self.init_money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.cards = Cards([Card(-1,-1),Card(-1,-1)])
        self.bet_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.status = 'call'
    
    def reset(self):
        self.money = self.init_money
        self.cards = Cards([Card(-1,-1),Card(-1,-1)])
        self.bet_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.status = 'call'
        
    def reset_for_a_cycle(self):
        self.cards = Cards([Card(-1,-1),Card(-1,-1)])
        self.bet_in_the_cycle = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.status = 'call' if self.money > 0 else 'fold'
        
    def reset_for_a_round(self):
        self.bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        if self.status == 'fold': self.status = 'fold'
        elif self.money == 0: self.status = 'all_in'
        else: self.status = 'call'
        
    def calculate_bet_and_raise_(self,bet):
        if bet >= self.bet_in_the_round:
            raise_ = min(self.money,bet-self.bet_in_the_round)
            bet = self.bet_in_the_round + raise_
            self.bet_in_the_round += raise_
            self.bet_in_the_cycle += raise_
            self.money -= raise_
        elif bet < self.bet_in_the_round:
            if bet == 0:
                self.bet_in_the_round = 0
                raise_ = 0
            else:
                print(self.bet_in_the_round,bet)
                raise ValueError('There is something Wrong!')
        return bet,raise_
    
    def change_status(self,bet,info):
        if bet > info['smallest_bet_in_the_round']: self.status = 'raise_'
        elif self.money == 0: self.status = 'all_in'
        elif bet == info['smallest_bet_in_the_round']:
            if info['current_player'] != info['raiser']: self.status = 'call'
            else: self.status = 'raise_'
        elif bet < info['smallest_bet_in_the_round']:
            if bet == 0: self.status = 'fold'
            else: 
                print(bet,info['smallest_bet_in_the_round'])
                raise ValueError('There is something wrong!')
    
    def action(self,state,reward,info):
        if info['round'] == 0 and info['pay_sb'] == False: bet = info['bb']/2
        elif info['round'] == 0 and info['pay_bb'] == False: bet = info['bb']
        else: bet = self.model(state,reward,info,self.money)
        bet = round(bet, len(decimal_precision)-2)
        bet,raise_ = self.calculate_bet_and_raise_(bet)
        self.change_status(bet,info)
        return {'bet':bet, 'raise_':raise_}
        
    def __str__(self):
        cards_info = ' and '.join(['%s'%(cards) for cards in self.cards])
        line_1 = f'players_{self.seat}[{self.status}] has {self.money} dollar. players_{self.seat} has betted {self.bet_in_the_round} in the round and betted {self.bet_in_the_cycle} in the clcye.'
        line_2 = f'players_{self.seat}[{self.status}] has {cards_info}.'
        return line_1
        
    def __repr__(self):
        cards_info = ' and '.join(['%s'%(cards) for cards in self.cards])
        line_1 = f'players_{self.seat}[{self.status}] has {self.money} dollar. players_{self.seat} has betted {self.bet_in_the_round} in the round and betted {self.bet_in_the_cycle} in the clcye.'
        line_2 = f'players_{self.seat}[{self.status}] has {cards_info}.'
        return line_1


class Players:
    def __init__(self,algos,player_number,money):
        self.player_number = player_number
        self.money = Decimal(money).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.players = [Player(seat=seat,money=money) for seat in range(self.player_number)]
    
    @property
    def alive_players_num(self):
        return sum((1 for player in self.players if player.money > 0))
    
    def reset(self):
        for player in self.players: player.reset()
            
    def reset_for_a_cycle(self):
        for player in self.players: player.reset_for_a_cycle()
            
    def reset_for_a_round(self):
        for player in self.players: player.reset_for_a_round()
            
    def take_cards(self,cards):
        for player in self.players:
            if player.money > 0:
                player.cards = cards.withdraw_cards(2)
    
    def check_raiser(self,info):
        if self.players[info['current_player']].status != 'raise_': return
        for player in self.players:
            if player != self.players[info['current_player']] and player.status == 'raise_':
                player.status = 'call' if player.money != 0 else 'all_in'
            else:
                pass # there is nothing to change.
    
    def show(self,action,info):
        bet_or_fold = 'fold' if self.players[info['current_player']].status == 'fold' else 'bet'
        if bet_or_fold == 'fold': print('player_%d fold!'%(info['current_player']))
        elif action['bet'] > info['smallest_bet_in_the_round']: print('player_%d raise %f dollar!'%(info['current_player'],action['bet']))
        else: print('player_%d bet %f dollar!'%(info['current_player'],action['bet']))
        print(self)
    
    def action(self,state,reward,info):
        action = self.players[info['current_player']].action(state,reward,info)
        self.check_raiser(info)
        self.show(action,info)
        return action
    
    def __len__(self):
        return self.player_number
    
    def __getitem__(self,idx):
        return self.players[idx]
    
    def __str__(self):
        return '\n'.join(['%s'%(player) for player in self.players if player.cards != None])
    
    def __repr__(self):
        return '\n'.join(['%s'%(player) for player in self.players if player.cards != None])


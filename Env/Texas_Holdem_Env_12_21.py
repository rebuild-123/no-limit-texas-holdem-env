from gym import Env
from random import choice
from utils import Deck, decimal_precision
from decimal import Decimal, ROUND_HALF_DOWN


class Texas_Holdem_Env(Env):
    def __init__(self,player_number:int=6,bb:float=0.5):
        self.player_number = player_number
        self.observation_space = None
        self.action_space = None
        self.reward_range = None
        self.new_round = False
        self.deck = Deck()
        self.community_cards = None
        self.bb = Decimal(bb).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.bet = 0
        self.min_raise = bb
        self.dead_money = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.round = 0
        self.pay_bb = False
        self.reset_who_pay_sb_and_bb = False
        self.sb_payer = self.bb_payer = self.raiser = self.current_player = -1
        self.active_player_in_the_cycle = []
        self.alive_players = []
    
    def info(self):
        info = {
            'raiser': self.raiser,
            'bb': self.bb,
            'round': self.round,
            'sb_payer': self.sb_payer,
            'bb_payer': self.bb_payer,
            'current_player': self.current_player,
            'min_raise': self.min_raise,
            'bet': self.bet,
            'pay_bb': self.pay_bb,
            'coummunity_cards': self.community_cards,
            'new_round': self.new_round
        }
        return info
    
    def store_players(self,players):
        self.players = players
    
    def reset(self,reset_who_pay_sb_and_bb=True, give_players_cards=False):
        state = None
        reward = None
        stop = False
        self.new_round = False
        self.deck = Deck()
        self.community_cards = None
        self.bet = 0
        self.min_raise = self.bb
        self.dead_money = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.round = 0
        self.pay_bb = False
        self.reset_who_pay_sb_and_bb = reset_who_pay_sb_and_bb
        if self.reset_who_pay_sb_and_bb == True:
            self.sb_payer = self.bb_payer = self.raiser = self.current_player = -1
            self.alive_players = []
        else:
            self.alive_players = sorted([
                player.seat for player in self.players if player.money > 0 or player.has_betted != 0
            ])
            self.deal_with_sb_and_bb_payer()
        if give_players_cards == True: self.give_players_cards()
        info = self.info()
        return state,reward,stop,info
    
    def deal_with_sb_and_bb_payer(self):
        for i in range(1,self.player_number):
            if (self.sb_payer + i)%self.player_number in self.alive_players:
                next_sb_payer = (self.sb_payer + i)%self.player_number
                idx = self.alive_players.index(next_sb_payer)
                self.alive_players = self.alive_players[idx:] + self.alive_players[:idx]
                self.current_player = self.sb_payer = self.raiser = self.alive_players[0]
                self.bb_payer = self.alive_players[1]
                break
        else:
            raise ValueError('The bb payer dosen\'t exist!')
    
    def give_players_cards(self):
        alive_players_num = self.players.alive_players_num
        if len(self.deck) < alive_players_num*2:
            raise ValueError('There is no enough card for alive players!')
        else:
            self.players.take_cards(self.deck.withdraw_cards(alive_players_num*2))
    
    def check_raiser_and_min_raise(self,action):
        if action['bet'] > self.bet:
            self.raiser = self.current_player
            self.min_raise = max(self.min_raise, action['bet'] - self.bet)
            self.bet = action['bet']
        elif action['bet'] <= self.bet:
            pass
                
    def shift_alive_player(self,action):
        if (action['bet'] == 0 and self.bet != 0) or self.players[self.alive_players[0]].status == 'all_in':
            self.alive_players.pop(0)
        else:
            for idx,player in enumerate(self.alive_players[1:],1):
                if self.players[player].status in ['call','raise_']:
                    self.alive_players = self.alive_players[idx:] + self.alive_players[:idx]
                    break
            else:
                pass # one raises and others all in or fold
    
    def give_the_winner_money(self):
        winner = choice(self.alive_players)
        self.players[winner].money += self.dead_money
        for player in self.players:
            player.has_betted = 0
    
    def next_round(self):
        self.new_round = True
        num = sum((1 for player in self.players if player.status in ['raise_','call'] and player.money > 0))
        if self.round == 3 or num < 2:
            self.stop = True
        else:
            self.round += 1
            self.bet = 0
            self.min_raise = self.bb
            self.community_cards = self.deck.withdraw_cards(3 if self.round == 1 else 1)
            self.players.reset_for_a_round()
            self.alive_players = []
            for seat in range(self.sb_payer,self.player_number+self.sb_payer):
                seat = seat%(self.player_number)
                if self.players[seat].status == 'call': # because reset_for_a_round, there is no raiser.
                    self.alive_players.append(seat)
            self.players[self.alive_players[0]].status = 'raise_'
            self.raiser = self.alive_players[0]
            self.current_player = self.alive_players[0]
    
    def step(self,state,action):
        self.stop = False
        self.new_round = False
        if self.current_player == self.bb_payer: self.pay_bb = True
        self.check_raiser_and_min_raise(action)
        self.dead_money += action['raise_']
        self.shift_alive_player(action)
        self.current_player = self.alive_players[0]
        if self.current_player == self.raiser: self.next_round()
        if self.stop: self.give_the_winner_money()
        info = self.info()
        return None,None,self.stop,info


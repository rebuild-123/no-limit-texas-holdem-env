from gym import Env
from random import choice
from utils import Deck, decimal_precision, Cards
from decimal import Decimal, ROUND_HALF_DOWN
from Agents import Players


class Texas_Holdem_Env:
    def __init__(self,players:Players,bb:float=0.5):
        self.deck = Deck()
        self.players = players
        self.players_queue = list(range(len(self.players)))
        self.bb = Decimal(bb).quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.dead_money = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.smallest_bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.min_raise = self.bb
        self.current_player = len(self.players) - 1
        self.raiser = len(self.players) - 1
        self.sb_payer = len(self.players) - 1
        self.round = 0
        self.pay_sb = False
        self.pay_bb = False
        self.new_round = False
        self.community_cards = Cards([])
    
    def give_players_cards(self):
        num = self.players.alive_players_num*2
        if len(self.deck) < num: raise ValueError('There is no enough card for alive players!')
        self.players.take_cards(self.deck.withdraw_cards(num))
    
    def reset(self):
        self.deck = Deck()
        self.players.reset()
        self.give_players_cards()
        self.players_queue = list(range(len(self.players)))
        self.dead_money = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.smallest_bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.min_raise = self.bb
        self.current_player = len(self.players) - 1
        self.raiser = len(self.players) - 1
        self.sb_payer = len(self.players) - 1
        self.round = 0
        self.pay_sb = False
        self.pay_bb = False
        self.new_round = False
        self.community_cards = Cards([])
        
    def info(self):
        info = {
            'bb':self.bb,
            'current_player':self.current_player,
            'round': self.round,
            'smallest_bet_in_the_round':self.smallest_bet_in_the_round,
            'pay_sb':self.pay_sb,
            'pay_bb':self.pay_bb,
            'raiser':self.raiser,
            'min_raise':self.min_raise,
            'new_round':self.new_round
        }
        return info
    
    def shift_players_queue(self,players_queue):
        for idx,player_seat in enumerate(self.players_queue[1:],1):
            if player_seat == self.raiser:
                break
            if self.players[player_seat].status != 'fold' and self.players[player_seat].money > 0:
                break
        return players_queue[idx:] + players_queue[:idx]
    
    def shift_to_capable_of_betting(self,players_queue):
        for idx,player_seat in enumerate(self.players_queue):
            if self.players[player_seat].status != 'fold' and self.players[player_seat].money > 0:
                break
        return players_queue[idx:] + players_queue[:idx]
        
    def reset_for_a_cycle(self):
        self.deck = Deck()
        self.players.reset_for_a_cycle()
        self.give_players_cards()
        idx = (self.players_queue.index(self.sb_payer)+1)%len(self.players)
        self.players_queue = self.players_queue[idx:] + self.players_queue[:idx]
        self.players_queue = self.shift_to_capable_of_betting(self.players_queue)
        self.dead_money = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.smallest_bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
        self.min_raise = self.bb
        self.current_player = self.players_queue[0]
        self.raiser = self.players_queue[0]
        self.sb_payer = self.players_queue[0]
        self.round = 0
        self.pay_sb = False
        self.pay_bb = False
        self.new_round = False
        self.community_cards = Cards([])
        return None,None,False,self.info() # state,reward,stop,info
    
    def deal_with_pay_sb_or_bb(self):
        self.pay_bb = self.pay_sb
        self.pay_sb = True
    
    def check_raiser_and_min_raise(self,action):
        if action['bet'] > self.smallest_bet_in_the_round:
            self.raiser = self.current_player
            self.min_raise = max(self.min_raise, action['bet'] - self.smallest_bet_in_the_round)
            self.smallest_bet_in_the_round = action['bet']
        else:
            pass # do nothing
    
    def next_round(self):
        self.new_round = True
        num = sum((1 for player in self.players if player.status in ['call','raise_'] and player.money > 0))
        if self.round == 3 or num < 2:
            self.stop = True
        else:
            self.players.reset_for_a_round()
            self.round += 1
            idx = self.players_queue.index(self.sb_payer)
            self.players_queue = self.players_queue[idx:] + self.players_queue[:idx]
            self.players_queue = self.shift_to_capable_of_betting(self.players_queue)
            self.smallest_bet_in_the_round = Decimal('0').quantize(Decimal(decimal_precision), rounding=ROUND_HALF_DOWN)
            self.min_raise = self.bb
            self.current_player = self.players_queue[0]
            self.raiser = self.players_queue[0]
            self.community_cards += self.deck.withdraw_cards(3 if self.round == 1 else 1)
    
    def deal_with_overbet(self):
        bet = [player.bet_in_the_cycle for player in self.players]
        idx = bet.index(max(bet))
        second_largest = max(bet[:idx] + bet[idx+1:])
        diff = max(bet) - second_largest
        self.players[idx].bet_in_the_cycle -= diff
        self.players[idx].bet_in_the_round -= diff
        self.players[idx].money += diff
        self.dead_money -= diff
        
    def rank_winners(self):
        rank_dic = {}
        for player in self.players:
            if player.status != 'fold':
                info = (player.cards + self.community_cards).sort().best_combination()
                rank_dic.setdefault((info['type'],info['rank']),[]).append(player.seat)
        winners_info = sorted(rank_dic.items(),key=lambda x:[-x[0][0],-x[0][1]])
        return winners_info
    
    def give_winner_money(self):
        self.community_cards += self.deck.withdraw_cards(5 - len(self.community_cards))
        self.deal_with_overbet()
        winners_info = self.rank_winners()
        print('community_cards are',str(self.community_cards.sort()).split('\n'))
        for player in self.players: 
            if player.status == 'fold': continue
            cards = str(player.cards.sort()).split("\n")
            print(f'player_{player.seat} has {cards}')
        for (type_,rank),winners in winners_info:
            if self.dead_money == 0: break
            for remove,winner in enumerate(winners):
                info = (self.players[winner].cards + self.community_cards).sort().best_combination()
                print(Cards(info['best_comp']))
                print(info['name'],info['rank'])
                winner_bet_in_the_cycle = self.players[winner].bet_in_the_cycle
                for player in self.players:
                    prize = min(winner_bet_in_the_cycle,player.bet_in_the_cycle)
                    prize = round(prize/(len(winners)-remove),len(decimal_precision)-2)
                    player.bet_in_the_cycle -= prize
                    self.dead_money -= prize
                    self.players[winner].money += prize
                    print(f'player_{winner} win {prize} from player_{player.seat}')
    
    def show(self,info):
        if info['new_round'] == True and not self.stop:
            print('\n-----new_round-----')
            print(self.community_cards)
            print('-------------------')
        print()
    
    def step(self,state,action):
        self.stop = self.new_round = False
        self.deal_with_pay_sb_or_bb()
        self.dead_money += action['raise_']
        self.check_raiser_and_min_raise(action)
        print('the raiser is ',self.raiser)
        self.players_queue = self.shift_players_queue(self.players_queue)
        self.current_player = self.players_queue[0]
        if self.current_player == self.raiser: self.next_round()
        if self.stop: self.give_winner_money()
        info = self.info()
        self.show(info)
        return None,None,self.stop,info


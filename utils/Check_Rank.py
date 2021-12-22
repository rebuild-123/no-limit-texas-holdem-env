from random import sample,shuffle
from collections import Counter
from .Card import Card

def straight_flush(cards):
    for card in cards[:3]:
        best_comp = [card]
        for number in range(card.number-1,card.number-5,-1):
            check_card = Card(card.suit,number)
            best_comp.append(check_card)
            if number < 0 or check_card not in cards:
                break
        else:
            return {'check':True,'type':20,'rank':card.number,'name':'straight_flush','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}                
                
def straight_flush_from_A_to_five(cards):
    for suit in range(4):
        best_comp = []
        for number in [12,3,2,1,0]:
            check_card = Card(suit,number)
            best_comp.append(check_card)
            if check_card not in cards:
                break
        else:
            return {'check':True,'type':19,'rank':0,'name':'straight_flush_from_A_to_five', 'best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def four_of_a_kind(cards):
    numbers = [card.number for card in cards]
    for number in set(numbers):
        if numbers.count(number) == 4:
            rank = number*100 + max([num for num in numbers if num != number])
            best_comp = [Card(suit,number) for suit in range(4)]
            best_comp += [card for card in cards if card not in best_comp][:1]
            best_comp.sort(reverse = True)
            return {'check':True,'type':18,'rank': rank,'name':'four_of_a_kind','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def full_house(cards):
    numbers = [card.number for card in cards]
    for three in numbers:
        if numbers.count(three) == 3:
            for two in numbers:
                if three != two and numbers.count(two) >= 2:
                    best_comp = [card for card in cards if card.number == three]
                    best_comp += [card for card in cards if card.number == two][:2]
                    best_comp.sort(reverse = True)
                    return {'check':True,'type':17,'rank':three*100+two,'name':'full_house', 'best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def flush(cards):
    suits = [card.suit for card in cards]
    for suit in set(suits):
        if suits.count(suit) >= 5:
            rank = 0
            best_comp = []
            for idx,card in enumerate([card for card in cards if card.suit == suit]):
                rank = rank*100 + card.number
                best_comp.append(card)
                if idx == 4: return {'check':True,'type':16,'rank':rank,'name':'flush','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def straight(cards):
    numbers = [card.number for card in cards]
    for card in cards[:3]:
        rank = card.number
        best_comp = [card]
        for number in range(card.number-1,card.number-5,-1):
            rank = rank*100 + number
            if number not in numbers or number < 0:
                break
            best_comp.append(cards[numbers.index(number)])
        else:
            return {'check':True,'type':15,'rank':rank,'name':'straight','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def straight_from_A_to_five(cards):
    numbers = [card.number for card in cards]
    best_comp = []
    for number in [12,3,2,1,0]:
        if number not in numbers:
            break
        best_comp.append(cards[numbers.index(number)])
    else:
        return {'check':True,'type':14,'rank':0,'name':'straight_from_A_to_five','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def three_of_a_kind(cards):
    numbers = [card.number for card in cards]
    for number in set(numbers):
        if numbers.count(number) == 3:
            for_rank = [num for num in numbers if num != number]
            rank = number*10000 + for_rank[0]*100 + for_rank[1]
            best_comp = [Card(suit,number) for suit in range(4) if Card(suit,number) in cards]
            best_comp += [card for card in cards if card not in best_comp][:2]
            best_comp.sort(reverse = True)
            return {'check':True,'type':13,'rank': rank,'name':'three_of_a_kind','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}
    
def two_pairs(cards):
    numbers = list(set([card.number for card in cards]))
    rank = count = 0
    best_comp = []
    for key,value in Counter([card.number for card in cards]).items():
        if value == 2:
            rank = rank*100 + key
            count += 1
            numbers.remove(key)
            best_comp += [Card(suit,key) for suit in range(4) if Card(suit,key) in cards]
        if count == 2: 
            best_comp += [card for card in cards if card not in best_comp][:1]
            best_comp.sort(reverse = True)
            return {'check':True,'type':12,'rank': rank*100+max(numbers),'name':'two_pairs', 'best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}

def pair(cards):
    numbers = [card.number for card in cards]
    rank = 0
    best_comp = []
    for pair_number in numbers:
        if numbers.count(pair_number) == 2:
            rank = rank*100 + pair_number
            count = 0
            best_comp += [Card(suit,pair_number) for suit in range(4) if Card(suit,pair_number) in cards]
            for number in numbers:
                if number != pair_number:
                    rank = rank*100 + number
                    count += 1
                if count == 4: 
                    best_comp += [card for card in cards if card not in best_comp][:4]
                    best_comp.sort(reverse = True)
                    return {'check':True,'type':11,'rank': rank,'name':'pair','best_comp':best_comp}
    return {'check':False,'type':None,'rank':None,'name':None,'best_comp':None}
    
def highcard(cards):
    rank = 0
    for number in [card.number for idx,card in enumerate(cards) if idx < 5]:
        rank = rank*100 + number
    return {'check':True,'type':10,'rank': rank,'name':'highcard','best_comp':cards[:5]}
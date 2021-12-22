from random import sample,shuffle 

def test_straight_flush():
    for suit in range(4):
        for start_number in range(9):
            cards = []
            for number in range(start_number,start_number+5):
                cards.append(Card(suit,number))
            suit = (suit+1)%4
            for number in sample(range(13),k=2):
                cards.append(Card(suit,number))
            cards = Cards(cards).sort()
            info = straight_flush(cards)
            if info['check'] == False:
                print(cards)
                raise ValueError('There is something wrong!')
    for suit in range(4):
        for start_number in range(10):
            cards = []
            for number in range(start_number,start_number+4):
                cards.append(Card(suit,number))
            suit = (suit+1)%4
            for number in sample(range(13),k=3):
                cards.append(Card(suit,number))
            cards = Cards(cards).sort()
            info = straight_flush(cards)
            if info['check'] == True:
                print(cards)
                raise ValueError('There is something wrong!')

def test_straight_flush_from_A_to_five():
    for suit in range(4):
        cards = []
        for number in [12,0,1,2,3]:
            cards.append(Card(suit,number))
        candidates = list(range(52))
        shuffle(candidates)
        for cand in candidates:
            card = Card(*divmod(cand,13))
            if card not in cards: cards.append(card)
            if len(cards) == 7: break
        cards = Cards(cards).sort()
        info = straight_flush_from_A_to_five(cards)
        if info['check'] == False:
            print(cards)
            raise ValueError('There is something wrong!')
    for suit in range(4):
        cards = []
        numbers = [12,0,1,2,3]
        shuffle(numbers)
        for number in numbers:
            cards.append(Card(suit,number))
        candidates = list(range(52))
        shuffle(candidates)
        for cand in candidates:
            card = Card(*divmod(cand,13))
            if card not in cards: cards.append(card)
            if len(cards) == 8: break
        cards = Cards(cards[1:]).sort()
        info = straight_flush_from_A_to_five(cards)
        if info['check'] == True:
            print(cards)
            raise ValueError('There is something wrong!')

def test_four_of_a_kind():
    for number in range(13):
        cards = [Card(suit,number) for suit in range(4)]
        for card_number in range(52):
            card = Card(*divmod(card_number,13))
            if card not in cards: cards.append(card)
            if len(cards) == 7: break
        cards = Cards(cards).sort()
        info = four_of_a_kind(cards)
        if info['check'] == False:
            print(cards)
            raise ValueError('There is something wrong!')
    for number in range(13):
        cards = [Card(suit,number) for suit in sample(list(range(4)),k=3)]
        for card_number in range(52):
            card = Card(*divmod(card_number,13))
            if card not in cards and card.number != cards[0].number: cards.append(card)
            if len(cards) == 7: break
        cards = Cards(cards).sort()
        info = four_of_a_kind(cards)
        if info['check'] == True:
            print(cards)
            raise ValueError('There is something wrong!')

def test_full_house():
    for three in range(13):
        for two in range(13):
            if two == three: continue
            cards = [Card(suit,three) for suit in sample(range(4),k=3)]
            cards.extend([Card(suit,two) for suit in sample(range(4),k=2)])
            for card_number in range(52):
                temp_card = Card(*divmod(card_number,13))
                if (card_number%13 != three) and (temp_card not in cards): cards.append(temp_card)
                if len(cards) == 7: break
        info = full_house(cards)
        if info['check'] == False:
            print(cards)
            raise ValueError('There is something wrong!')
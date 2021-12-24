# no-limit-texas-holdem-env
## main.ipynb
```python3
import json
from Agents import Players
from Env import Texas_Holdem_Env

with open('./Config.json','r') as fp:
    config = json.load(fp)
```
```python3
count = 0
players = Players(algos=config['algos'],player_number=config['player_number'],money=config['money']) # create agents
env = Texas_Holdem_Env(players=players,bb=config['bb']) # create environment

while config['epochs'] > count:
    env.reset() # reset environment for each epoch
    while players.alive_players_num > 1: # count the number of players whose money is more than zero.
        state,reward,stop,info = env.reset_for_a_cycle() # reset_for_a_cycle for each cycle
        while not stop: # when the round is stopped, "stop" will be True. a cycle has four rounds, which are "preflop"、"flop"、"turn" and "river".
            action = players.action(state,reward,info) # a player takes state from environment and makes an action.
            state,reward,stop,info = env.step(state,action) # the environment changes with the action from players.
        print('\n\n')
    count += 1
```
## result
```
player_3 raise 0.250000 dollar!
players_0[call] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[call] has 0.4800000 dollar. players_1 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 2.0850000 dollar. players_3 has betted 0.2500000 in the round and betted 0.2500000 in the clcye.
players_4[call] has 6.3529000 dollar. players_4 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_5[call] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_4 raise 0.500000 dollar!
players_0[call] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[call] has 0.4800000 dollar. players_1 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[call] has 2.0850000 dollar. players_3 has betted 0.2500000 in the round and betted 0.2500000 in the clcye.
players_4[raise_] has 5.8529000 dollar. players_4 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_5[call] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_5 fold!
players_0[call] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[call] has 0.4800000 dollar. players_1 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[call] has 2.0850000 dollar. players_3 has betted 0.2500000 in the round and betted 0.2500000 in the clcye.
players_4[raise_] has 5.8529000 dollar. players_4 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_0 fold!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[call] has 0.4800000 dollar. players_1 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[call] has 2.0850000 dollar. players_3 has betted 0.2500000 in the round and betted 0.2500000 in the clcye.
players_4[raise_] has 5.8529000 dollar. players_4 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_1 bet 0.480000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0.4800000 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[call] has 2.0850000 dollar. players_3 has betted 0.2500000 in the round and betted 0.2500000 in the clcye.
players_4[raise_] has 5.8529000 dollar. players_4 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_3 bet 0.500000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0.4800000 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[call] has 1.8350000 dollar. players_3 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_4[raise_] has 5.8529000 dollar. players_4 has betted 0.5000000 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

--------new_round--------
-----community_cards-----
Card(suit=heart  , number=Q )
Card(suit=club   , number=8 )
Card(suit=diamond, number=6 )
-------------------------

player_3 bet 0.000000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 1.8350000 dollar. players_3 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_4[call] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_4 bet 0.000000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 1.8350000 dollar. players_3 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_4[call] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

--------new_round--------
-----community_cards-----
Card(suit=heart  , number=Q )
Card(suit=club   , number=8 )
Card(suit=diamond, number=6 )
Card(suit=spade  , number=9 )
-------------------------

player_3 bet 0.000000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 1.8350000 dollar. players_3 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_4[call] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_4 bet 0.000000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 1.8350000 dollar. players_3 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_4[call] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

--------new_round--------
-----community_cards-----
Card(suit=heart  , number=Q )
Card(suit=club   , number=8 )
Card(suit=diamond, number=6 )
Card(suit=spade  , number=9 )
Card(suit=club   , number=Q )
-------------------------

player_3 raise 1.230000 dollar!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 0.6050000 dollar. players_3 has betted 1.2300000 in the round and betted 1.7300000 in the clcye.
players_4[call] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

player_4 fold!
players_0[fold] has 10.3150000 dollar. players_0 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_1[all_in] has 0E-7 dollar. players_1 has betted 0E-7 in the round and betted 0.4800000 in the clcye.
players_2[fold] has 0E-7 dollar. players_2 has betted 0E-7 in the round and betted 0E-7 in the clcye.
players_3[raise_] has 0.6050000 dollar. players_3 has betted 1.2300000 in the round and betted 1.7300000 in the clcye.
players_4[fold] has 5.8529000 dollar. players_4 has betted 0E-7 in the round and betted 0.5000000 in the clcye.
players_5[fold] has 4.5171000 dollar. players_5 has betted 0E-7 in the round and betted 0E-7 in the clcye.

---------the_cycle_is_over---------
community_cards are ['Card(suit=heart  , number=Q )', 'Card(suit=club   , number=Q )', 'Card(suit=spade  , number=9 )', 'Card(suit=club   , number=8 )', 'Card(suit=diamond, number=6 )']
player_1, has ['Card(suit=diamond, number=A )', 'Card(suit=spade  , number=Q )']
player_3, has ['Card(suit=club   , number=A )', 'Card(suit=diamond, number=10)']

------------winners'information------------
the name of player_1's winning cards combination is three_of_a_kind
the rank of player_1's winning cards combination is 101207
---------winning cards combination---------
Card(suit=diamond, number=A )
Card(suit=spade  , number=Q )
Card(suit=heart  , number=Q )
Card(suit=club   , number=Q )
Card(suit=spade  , number=9 )
------------win the prize from------------
player_1 win 0E-7 from player_0
player_1 win 0.4800000 from player_1
player_1 win 0E-7 from player_2
player_1 win 0.4800000 from player_3
player_1 win 0.4800000 from player_4
player_1 win 0E-7 from player_5

------------winners'information------------
the name of player_3's winning cards combination is pair
the rank of player_3's winning cards combination is 1012080706
---------winning cards combination---------
Card(suit=club   , number=A )
Card(suit=heart  , number=Q )
Card(suit=club   , number=Q )
Card(suit=diamond, number=10)
Card(suit=spade  , number=9 )
Card(suit=club   , number=8 )
------------win the prize from------------
player_3 win 0E-7 from player_0
player_3 win 0E-7 from player_1
player_3 win 0E-7 from player_2
player_3 win 0.0200000 from player_3
player_3 win 0.0200000 from player_4
player_3 win 0E-7 from player_5
```

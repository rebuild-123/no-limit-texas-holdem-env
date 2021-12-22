#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from random import randint,random


# In[ ]:


class Sudo_Model:
    def __init__(self):
        pass
    def __call__(self,state,reward,info,money):
        rand = random()
        if rand < 0.7:
            return 0
        elif 0.7 <= rand < 0.9:
            return info['bet']
        else:
            return info['bet'] + info['min_raise']*randint(100,300)/100


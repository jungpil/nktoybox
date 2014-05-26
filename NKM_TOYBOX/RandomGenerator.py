'''
Created on 2014. 2. 3.

@author: drtagkim
'''
import numpy as np
import random as rd

myCurrentSeed = 0
random_generator = np.random.RandomState() # Mersenne Twister Pesudo-random Generator
random_generator_nextLong = rd.randint # (min,max) e.g., (0,1) -> (0,1,0,0,1,1,..)
random_generator_nextDouble = rd.random

def set_seed(seed_number_range): # static method (cause there is no static class in Python...)
    global myCurrentSeed
    myCurrentSeed = seed_number_range
    random_generator = np.random.RandomState(seed_number_range)
def get_current_seed():
    return myCurrentSeed
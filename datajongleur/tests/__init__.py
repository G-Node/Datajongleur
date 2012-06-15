import datajongleur as dj
from datajongleur.beanbags.models import *
from datajongleur.beanbags.neuro.models import *
from datajongleur.addendum.models import *
import numpy as np
import random

session = dj.get_session()

numbers = []
numbers2 = []
numbers_int = []
units = []
time_units = ['s', 'ms', 'us', 'ns', 'ps']

for idx in range(4):
    numbers.append(random.random())
    numbers2.append(random.random())
    numbers_int.append(random.randint(0, 10))
    units.append(random.choice(time_units))

np_numbers = np.array(numbers)
np_numbers2 = np.array(numbers2)
np_numbers_int = np.array(numbers_int)
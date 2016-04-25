# -*- coding: utf-8 -*-
from math import *
import sys
import random

def choose(candidates, probabilities):
    probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
    if probabilities[-1] > 1.0:
        probabilities = [x/probabilities[-1] for x in probabilities]
        rand = random.random()
        for candidate, probability in zip(candidates, probabilities):
            if rand < probability:
                return candidate
        return None

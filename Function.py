# -*- coding: utf-8 -*-

## 
# @file Function.py
# @Synopsis common funtion
# @author Gong Chen <jie211.jp@gmail.com>
# @version 1.0
# @date 2016-04-25
# This is free and unencumbered code released into the public domain.

from math import *
import sys
import random

# -------------------------------
## 
# @Synopsis  choose 重み付きランダムを出す
# 
# @Param 候補リスト
# @Param 確率
# 
# @Returns 選択結果  
# ---------------------------------
def choose(candidates, probabilities):
    probabilities = [sum(probabilities[:x+1]) for x in range(len(probabilities))]
    if probabilities[-1] > 1.0:
        probabilities = [x/probabilities[-1] for x in probabilities]
        rand = random.random()
        for candidate, probability in zip(candidates, probabilities):
            if rand < probability:
                return candidate
        return None

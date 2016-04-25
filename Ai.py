# -*- coding: utf-8 -*-
from math import *
import sys
import random

from Othello import Othello
from Node import Node
from Function import choose
import operator

def MCTS(rootgame, times, verbose=False):

    rootnode = Node(game = rootgame)

    for i in xrange(times):
        node = rootnode
        game = rootgame.DeepCopy(rootgame.size)

        #selection
        while node.canMoveStep == [] and node.childNode != []:
            node = node.UCT()
            game.DoMove(node.move)

        #expansion
        if node.canMoveStep != []:
            m = random.choice(node.canMoveStep)
            game.DoMove(m)
            node = node.AddChild(m, game)

        #simulation
        while game.GetCanMove() != []:
            game.DoMove(random.choice(game.GetCanMove()))

        #backpropagation
        while node != None:
            node.Upload(game.GetScore(node.lastMoved))
            node = node.parentNode

    if verbose:
        print rootnode.GetTree(0)
    else:
        pass
        # print rootnode.GetChild()

    valueable = sorted(rootnode.childNode, key = lambda i: i.visit)[-1].move
    return valueable

def MC(game, times, verbose=False):
    candidates = game.GetCanMove()
    points = {}
    for i in candidates:
        index = i[0]*10 + i[1]
        re = [index/10, index%10]

        if not points.has_key(index):
            points[index]=0

        for j in xrange(times):
            thisgame=game.DeepCopy(game.size)
            thisgame.DoMove(i)
            player = thisgame.lastMoved
            while thisgame.GetCanMove() != []:
                thisgame.DoMove(random.choice(thisgame.GetCanMove()))
            points[index]+=thisgame.GetScore(player)

    get_max = max(points.iteritems(), key=operator.itemgetter(1))[0]
    max_position = [get_max/10, get_max%10]
    if verbose:
        print "score-> " + str(points)
        print "best-> " + str(get_max)
    return max_position

def RandAI(game):
    candidate = game.GetCanMove()
    return random.choice(candidate)

def ScoreMax(game):
    candidate = game.GetCanMove()
    points = {}
    for i in candidate:
        thisgame=game.DeepCopy(game.size)
        thisgame.DoMove(i)
        p=thisgame.GetPoint(game.lastMoved)
        if not points.has_key(p):
            points[p]=[]
        points[p].append(i)

    max_point = max(points)
    max_candidate = points[max_point]
    return random.choice(max_candidate)

def Less_chance(game):
    candidates = game.GetCanMove()
    points = {}
    for i in candidates:
        thisgame = game.DeepCopy(game.size)
        thisgame.DoMove(i)
        c = len(thisgame.GetCanMove())
        print c
        if not points.has_key(c):
            points[c]=[]
        points[c].append(i)

    min_chance = min(points)
    print "min is "+str(min_chance)
    min_candidate = points[min_chance]
    return random.choice(min_candidate)

def ProbabilitySelect(game):
    all_candidates = game.GetCanMove()
    plan = choose([1, 2, 3], [0.7, 0.2, 0.2])
    print plan
    if plan == 1:
        print "do scoremax"
        return ScoreMax(game)
    elif plan == 2:
        print "do randai"
        return RandAI(game)
    elif plan == 3:
        print "do lesschance"
        return Less_chance(game)

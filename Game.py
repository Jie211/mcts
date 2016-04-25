# -*- coding: utf-8 -*-
from math import *
import sys
import random

from Node import Node
from Othello import Othello
from Ai import *
    
def PlayGame():
    # verbose1 = False
    verbose1 = True

    verbose2 = False
    # verbose2 = True

    Wtotalwin = 0
    Btotalwin = 0

    testtime = 1
    nowtime = 0

    while( nowtime < testtime  ):
    
        game = Othello(6)

        while(game.GetCanMove() != []):
            if verbose1 : 
                print repr(game)
                print 'Can->'+str(game.GetCanMove())
            if game.lastMoved == 'B':
                # -> white
                # m = MCTS(rootgame = game, times = 100, verbose = verbose2)
                # m = RandAI(game) 
                # m = ScoreMax(game) 
                m = MC(game, 100, verbose = verbose2) 
                # m = ProbabilitySelect(game) 
                # m = Less_chance(game) 
                if verbose1 : print "W",
            else:
                # -> black
                m = MCTS(rootgame = game, times = 50, verbose = verbose2)
                # m = RandAI(game)
                if verbose1 : print "B",
            game.DoMove(m)
            if verbose1 : print "Do-> "+str(m)+"\n"

        # if verbose1:
        #     print str(game)
        #     print game.GetPoint(game.lastMoved)
        #     print game.GetPoint(game.GetOpponent(game.lastMoved))

        if game.GetScore(game.lastMoved) == 1.0:
            print str(game.lastMoved) + " win"
            if game.lastMoved == 'W':
                Wtotalwin+=1
            else:
                Btotalwin+=1
        elif game.GetScore(game.lastMoved) == 0.0:
            print str(game.GetOpponent(game.lastMoved)) + " win"
            if game.lastMoved == 'W':
                Btotalwin+=1
            else:
                Wtotalwin+=1
        else:
            print "draw"
        
        nowtime+=1
        print "--------------------"
        print "White : "+str(Wtotalwin)
        print "Black : "+str(Btotalwin)

# -*- coding: utf-8 -*-

## 
# @file PlayGame.py
# @Synopsis ゲーム全体の流れ
# @author Gong Chen <jie211.jp@gmail.com>
# @version 1.0
# @date 2016-04-25
# This is free and unencumbered code released into the public domain.

from math import *
import sys
import random

from Node import Node
from Othello import Othello
from Ai import *
    
def PlayGame():
    verbose1 = False
    # verbose1 = True

    verbose2 = False
    # verbose2 = True

    Wtotalwin = 0
    Btotalwin = 0

    testtime = 1
    nowtime = 0

    while( nowtime < testtime  ):
    
        #8x8のオセロのゲームを生成する
        game = Othello(8)

        #まだ打てる手があるならゲームを続ける
        while(game.GetCanMove() != []):
            if verbose1 : 
                print repr(game)
                print 'Can->'+str(game.GetCanMove())
            
            #使えるAI
            # MCTS(rootgame=game, times=100, verbose=False)
            # MC(rootgame=game, times=100, verbose=False)
            # ScoreMax(gmae)
            # ProbabilitySelect(game)
            # Less_chance(game)
            # RandAI(game)

            if game.lastMoved == 'B':
                #  white 白のAI
                m = MC(game, 100, False) 
                if verbose1 : print "W",
            else:
                # black 黒のAI
                m = RandAI(game)
                if verbose1 : print "B",
            game.DoMove(m)
            if verbose1 : print "Do-> "+str(m)+"\n"

        #勝敗の表示
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

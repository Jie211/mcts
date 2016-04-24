#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:   jie211
# URL:      http://jie211.github.io
# License:  MIT License
# Created:  2016-04-23
#
from math import *
import sys
import random

class Othello:
    def __init__ (self, size):
        self.size = size
        assert size == int(size) and size % 2 == 0, "size must be integer and even number."
        self.board = [['N' for i in xrange(size)] for j in xrange(size)]
        self.lastMoved = 'W'
        self.board[size/2][size/2] = self.board[size/2-1][size/2-1] = 'B'
        self.board[size/2][size/2-1] = self.board[size/2-1][size/2] = 'W'

    def GetCanMove(self):
        # l=[]
        # for i in xrange(self.size):
        #     for j in xrange(self.size):
        #         if self.board[i][j] == 'N' and self.IsCanFilp(i, j):
        #             l.append([i, j])
        # return l
        return [(x,y) for x in xrange(self.size) for y in xrange(self.size) if self.board[x][y] == 'N' and self.IsCanFilp(x, y)]

    def DeepCopy(self, size):
        o = Othello(self.size)
        o.lastMoved = self.lastMoved
        o.board = [self.board[i][:] for i in xrange(self.size)]
        o.size = self.size
        return o

    def DoMove(self, move):
        lastplayer=self.lastMoved
        nextplayer=self.GetOpponent(lastplayer)
        (x, y) = (move[0], move[1])
        assert x==int(x) and y==int(y)
        assert self.IsOnBoard(x,y)
        assert self.board[x][y]=='N'
        m = self.GetCanFilp(x, y)
        self.lastMoved = nextplayer
        self.board[x][y] = self.lastMoved
        for (i,j) in m:
            self.board[i][j] = self.lastMoved

    def IsCanFilp(self, x, y):
        for (dx, dy) in self.NearOpponentDirections(x, y):
            if len(self.GetFilpList(x, y, dx, dy)) > 0:
                return True
        return False

    def GetCanFilp(self, x, y):
        l=[]
        for (dx, dy) in self.NearOpponentDirections(x, y):
            l.extend(self.GetFilpList(x, y, dx, dy))
        return l

    def TryFilp(self, x, y):
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]:
            if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
                return True
        return False

    def GetFilpList(self, x, y, dx, dy):
        fl = []
        x += dx
        y += dy
        while self.IsOnBoard(x, y) and self.board[x][y] == self.lastMoved:
            fl.append((x, y))
            x += dx
            y += dy
        if self.IsOnBoard(x, y) and self.board[x][y] == self.GetOpponent(self.lastMoved):
            return fl
        else:
            return []
    
    def GetOpponent(self, player):
        assert player=='W' or player=='B'
        if player == 'W':
            return 'B'
        else:
            return 'W'

    def NearOpponentDirections(self, x, y):
        near = []
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]:
            if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
                near.append((dx, dy))
        return near

    def IsOnBoard(self, x, y):
        if x>=0 and x<self.size and y>=0 and y<self.size :
            return True
        else:
            return False

    def GetScore(self, player):
        thisplayer = player
        oppoplayer = self.GetOpponent(player)
        thisscore = len([ (i, j) for i in xrange(self.size) for j in xrange(self.size) if self.board[i][j] == thisplayer  ])
        opposcore = len([ (i, j) for i in xrange(self.size) for j in xrange(self.size) if self.board[i][j] == oppoplayer  ])
        if thisscore > opposcore:
            return 1.0
        elif thisscore < opposcore:
            return 0.0
        else:
            return 0.5

    def GetPoint(self, player):
        point = len([ (i, j) for i in xrange(self.size) for j in xrange(self.size) if self.board[i][j] == player  ])
        return str(player)+" "+str(point)

    def __repr__(self):
        s=""
        num=' '
        for i in xrange(self.size):
            num+=' '+str(i)
        s += num+"\n"
        # for y in xrange(self.size-1, -1, -1):
        for y in xrange(self.size):
            s += str(y)+"|"
            for x in xrange(self.size):
                if self.board[x][y] == 'N':
                    s += ' '
                elif self.board[x][y] == 'B':
                    s += '●'
                else:
                    s += '○'
                s += '|'
            s += "\n"
        return s
    
class Node:
    def __init__(self, move = None, parent = None, game = None):
        self.move = move
        self.parentNode = parent
        self.childNode = []
        self.win = 0
        self.visit = 0
        self.canMoveStep = game.GetCanMove()
        self.lastMoved = game.lastMoved

    def AddChild(self, m, g):
        newNode = Node(move = m, parent = self, game = g)
        self.canMoveStep.remove(m)
        self.childNode.append(newNode)
        return newNode

    def Upload(self, score):
        self.visit += 1
        self.win += score

    def UCT(self):
        value = sorted(self.childNode, key = lambda i : i.win/i.visit + sqrt( 2*log(self.visit)/i.visit ))[-1]
        return value

    def GetChild(self):
        s = ""
        for i in self.childNode:
            s += str(i)+"\n"
        return s
    
    def GetDeep(self, deep):
        s = "\n"
        for i in xrange(1, deep+1):
            s += "|_"
        return s

    def GetTree(self, deep):
        s = self.GetDeep(deep)+str(self)
        for i in self.childNode:
            s += i.GetTree(deep+1)
        return s

    def __repr__(self):
        return "+[ Move: " + str(self.move) + " NextCanMove: "+str(self.canMoveStep) +" Visit: " + str(self.visit) + " ]"

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
        print rootnode.GetChild()

    valueable = sorted(rootnode.childNode, key = lambda i: i.visit)[-1].move
    return valueable


def PlayGame():
    # AllVerbose = False
    AllVerbose = True
    game = Othello(6)

    while(game.GetCanMove() != []):
        if AllVerbose : 
            print str(game)
            print 'Can->'+str(game.GetCanMove())
        if game.lastMoved == 'B':
            m = MCTS(rootgame = game, times = 100, verbose=AllVerbose)
            if AllVerbose : print "W",
        else:
            m = MCTS(rootgame = game, times = 200, verbose=AllVerbose)
            if AllVerbose : print "B",
        game.DoMove(m)
        if AllVerbose : print "Do-> "+str(m)+"\n"

    if AllVerbose:
        print str(game)
        print game.GetPoint(game.lastMoved)
        print game.GetPoint(game.GetOpponent(game.lastMoved))

    if game.GetScore(game.lastMoved) == 1.0:
        print str(game.lastMoved) + " win"
    elif game.GetScore(game.lastMoved) == 0.0:
        print str(game.GetOpponent(game.lastMoved)) + " win"
    else:
        print "draw"

if __name__ == "__main__":
    PlayGame()

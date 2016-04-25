# -*- coding: utf-8 -*-
from math import *
import sys
import random

# from joblib import Parallel, delayed

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
        assert x==int(x) and y==int(y), "move index must be integer"
        assert self.IsOnBoard(x,y), "move must on board"
        assert self.board[x][y]=='N', "move position must be empty"
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

    # def TryFilp(self, x, y):
    #     for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]:
    #         if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
    #             return True
    #     return False

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

    def Process(self, i, x, y, direction):
        dx = direction[i][0]
        dy = direction[i][1]
        if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
            return (dx, dy)
        return None

    def NearOpponentDirections(self, x, y):
        near = []
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]:
            if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
                near.append((dx, dy))
        return near

        # near = []
        # direction = [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]
        # dir_len = len(direction)
        # for i in xrange(dir_len):
        #     dx=direction[i][0]
        #     dy=direction[i][1]
        #     if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
        #         near.append((dx, dy))
        # # print near
        # return near

        # near = []
        # direction = [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]
        # dir_len = len(direction)
        # # for i in xrange(dir_len):
        #     # get = self.Process(i, x, y, direction)
        #     # if get != None:near.append(get)
        # print Parallel(n_jobs=-1)([delayed(self.Process)(i, x, y, direction) for i in xrange(dir_len)])
        # return near



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
        # return str(player)+" "+str(point)
        return point

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


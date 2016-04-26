# -*- coding: utf-8 -*-

## 
# @file Othello.py
# @Synopsis  othello game
# @author Gong Chen <jie211.jp@gmail.com>
# @version 1.0
# @date 2016-04-25
# This is free and unencumbered code released into the public domain.

from math import *
import sys
import random

# from joblib import Parallel, delayed

class Othello:
# -------------------------------
## 
# @Synopsis  __init__ コンストラクタ
# 
# @Param 盤面サイズ
# 
# @Returns  なし 
# ---------------------------------
    def __init__ (self, size):
        self.size = size
        assert size == int(size) and size % 2 == 0 and size <= 9, "size must be integer and even number, size must <= 9."
        self.board = [['N' for i in xrange(size)] for j in xrange(size)]
        #盤面データにNが石なし, Bが黒, Wが白
        self.lastMoved = 'W'
        self.board[size/2][size/2] = self.board[size/2-1][size/2-1] = 'B'
        self.board[size/2][size/2-1] = self.board[size/2-1][size/2] = 'W'

# -------------------------------
## 
# @Synopsis  GetCanMove 打てる石を探す
# 
# @Returns  打てる石 
# ---------------------------------
    def GetCanMove(self):
        return [(x,y) for x in xrange(self.size) for y in xrange(self.size) if self.board[x][y] == 'N' and self.IsCanFilp(x, y)]

# -------------------------------
## 
# @Synopsis  DeepCopy 盤面をコピーする
# 
# @Param size
# 
# @Returns   
# ---------------------------------
    def DeepCopy(self, size):
        o = Othello(self.size)
        o.lastMoved = self.lastMoved
        o.board = [self.board[i][:] for i in xrange(self.size)]
        o.size = self.size
        return o

# -------------------------------
## 
# @Synopsis  DoMove 手を打つ
# 
# @Param 打つ場所
# 
# @Returns   
# ---------------------------------
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

# -------------------------------
## 
# @Synopsis  IsCanFilp ひっくり返すかどうかを確認する
# 
# @Param x x座標
# @Param y y座標
# 
# @Returns   
# ---------------------------------
    def IsCanFilp(self, x, y):
        for (dx, dy) in self.NearOpponentDirections(x, y):
            if len(self.GetFilpList(x, y, dx, dy)) > 0:
                return True
        return False

# -------------------------------
## 
# @Synopsis  GetCanFilp 全部のひっくり返し可能なリストを返す
# 
# @Param x
# @Param y
# 
# @Returns  リスト 
# ---------------------------------
    def GetCanFilp(self, x, y):
        l=[]
        for (dx, dy) in self.NearOpponentDirections(x, y):
            l.extend(self.GetFilpList(x, y, dx, dy))
        return l

# -------------------------------
## 
# @Synopsis  GetFilpList 一つの座標からひっくり返し石のリストを返す
# 
# @Param x
# @Param y
# @Param dx
# @Param dy
# 
# @Returns   
# ---------------------------------
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
    
# -------------------------------
## 
# @Synopsis  GetOpponent 相手の身分を返す
# 
# @Param player
# 
# @Returns   
# ---------------------------------
    def GetOpponent(self, player):
        assert player=='W' or player=='B'
        if player == 'W':
            return 'B'
        else:
            return 'W'


# -------------------------------
## 
# @Synopsis  NearOpponentDirections 周りに敵が存在するかどうか
# 
# @Param x
# @Param y
# 
# @Returns   
# ---------------------------------
    def NearOpponentDirections(self, x, y):
        near = []
        for (dx, dy) in [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]:
            if self.IsOnBoard(x+dx, y+dy) and self.board[x+dx][y+dy] == self.lastMoved:
                near.append((dx, dy))
        return near

        # near = []
        # direction = [(0, +1), (+1, +1), (+1, 0), (+1, -1), (0, -1), (-1, -1), (-1, 0), (-1, +1)]
        # dir_len = len(direction)
        # # for i in xrange(dir_len):
        #     # get = self.Process(i, x, y, direction)
        #     # if get != None:near.append(get)
        # print Parallel(n_jobs=-1)([delayed(self.Process)(i, x, y, direction) for i in xrange(dir_len)])
        # return near



# -------------------------------
## 
# @Synopsis  IsOnBoard 盤面にいるがどうか
# 
# @Param x
# @Param y
# 
# @Returns   
# ---------------------------------
    def IsOnBoard(self, x, y):
        if x>=0 and x<self.size and y>=0 and y<self.size :
            return True
        else:
            return False

# -------------------------------
## 
# @Synopsis  GetScore 勝敗をチェックする
# 
# @Param player
# 
# @Returns   
# ---------------------------------
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

# -------------------------------
## 
# @Synopsis  GetPoint 得点を計算する
# 
# @Param player
# 
# @Returns   
# ---------------------------------
    def GetPoint(self, player):
        point = len([ (i, j) for i in xrange(self.size) for j in xrange(self.size) if self.board[i][j] == player  ])
        # return str(player)+" "+str(point)
        return point

# -------------------------------
## 
# @Synopsis  __repr__ オブジェクトを文字列にする
# 
# @Returns   
# ---------------------------------
    def __repr__(self):
        s=""
        num=' '
        for i in xrange(self.size):
            num+=' '+str(i)
        s += num+"\n"
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


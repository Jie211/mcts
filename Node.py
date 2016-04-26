# -*- coding: utf-8 -*-

## 
# @file Node.py
# @Synopsis  Tree structure
# @author Gong Chen <jie211.jp@gmail.com>
# @version 1.0
# @date 2016-04-25
# This is free and unencumbered code released into the public domain.

from math import *
import sys
import random

class Node:
# -------------------------------
## 
# @Synopsis  __init__ コンストラクタ
# 
# @Param 打つ手
# @Param 親ノード
# @Param ゲームの状態
# 
# @Returns なし 
# ---------------------------------
    def __init__(self, move = None, parent = None, game = None):
        #打つ手
        self.move = move
        #親ノード
        self.parentNode = parent
        #子ノード
        self.childNode = []
        #勝った回数
        self.win = 0
        #アクセスされた回数
        self.visit = 0
        #候補
        self.canMoveStep = game.GetCanMove()
        #最後に打った手
        self.lastMoved = game.lastMoved

# -------------------------------
## 
# @Synopsis  AddChild 子ノードを追加
# 
# @Param 打つ手 
# @Param ゲーム状態
# 
# @Returns 生成した子ノード 
# ---------------------------------
    def AddChild(self, m, g):
        newNode = Node(move = m, parent = self, game = g)
        self.canMoveStep.remove(m)
        self.childNode.append(newNode)
        return newNode

# -------------------------------
## 
# @Synopsis  Upload プレイアウトの結果を逆伝播
# 
# @Param 点数
# 
# @Returns  なし
# ---------------------------------
    def Upload(self, score):
        self.visit += 1
        self.win += score

# -------------------------------
## 
# @Synopsis  UCT (UCB applied to Trees)
# 
# @Returns  算出した価値 
# ---------------------------------
    def UCT(self):
        #value = ノード勝った回数/ノードがアクセスされた回数 + sqrt( 2xlog(アクセスされた回数総数/ノードがアクセスされた回数)  )
        value = sorted(self.childNode, key = lambda i : i.win/i.visit + sqrt( 2*log(self.visit)/i.visit ))[-1]
        return value

# -------------------------------
## 
# @Synopsis  GetChild このノードを表示する
# 
# @Returns 文字列 
# ---------------------------------
    def GetChild(self):
        s = ""
        for i in self.childNode:
            s += str(i)+"\n"
        return s
    
# -------------------------------
## 
# @Synopsis  GetDeep 木の深さを表示する
# 
# @Param 深さ
# 
# @Returns 文字列  
# ---------------------------------
    def GetDeep(self, deep):
        s = "\n"
        for i in xrange(1, deep+1):
            s += "|_"
        return s

# -------------------------------
## 
# @Synopsis  GetTree 木構造を表示する
# 
# @Param 深さ
# 
# @Returns 文字列  
# ---------------------------------
    def GetTree(self, deep):
        s = self.GetDeep(deep)+str(self)
        for i in self.childNode:
            s += i.GetTree(deep+1)
        return s

# -------------------------------
## 
# @Synopsis  __repr__ オブジェクトを文字列にする
# 
# @Returns   
# ---------------------------------
    def __repr__(self):
        return "+[ Move: " + str(self.move) + " NextCanMove: " + str(self.canMoveStep) + " Visit: " + str(self.visit) + " ]"


# -*- coding: utf-8 -*-

## 
# @file Ai.py
# @Synopsis  ai for othello game
# @author Gong Chen <jie211.jp@gmail.com>
# @version 1.0
# @date 2016-04-25
# This is free and unencumbered code released into the public domain.

from math import *
import sys
import random

from Othello import Othello
from Node import Node
from Function import choose
import operator

# -------------------------------
## 
# @Synopsis  MCTS(MonteCarloTreeSearch)
# 
# @Param rootgame : ゲームの状態
# @Param times : プレイアウト回数
# @Param verbose : 冗長データ可視化
# 
# @Returns : 打つ手
# ---------------------------------
def MCTS(rootgame, times, verbose=False):
    
    #木を生成
    rootnode = Node(game = rootgame)

    #候補の数から各候補にかかるプレイアウト回数を計算
    len_candidate = len(rootnode.canMoveStep)

    for i in xrange(times * len_candidate):
        node = rootnode
        #プレイアウト毎にゲームの状態をコピーする
        game = rootgame.DeepCopy(rootgame.size)

        #価値があるノードの中からUCTで最も価値がある枝まで進む
        while node.canMoveStep == [] and node.childNode != []:
            node = node.UCT()
            game.DoMove(node.move)
        #試されていない候補はまだ残ってるなら候補から木を展開する
        if node.canMoveStep != []:
            m = random.choice(node.canMoveStep)
            game.DoMove(m)
            #展開された部分を今のノードの子ノードに追加する
            node = node.AddChild(m, game)
        #プレイアウト
        while game.GetCanMove() != []:
        #プレイアウトのpolicyはランダムとします
            game.DoMove(random.choice(game.GetCanMove()))

        #試合の結果を逆伝播
        while node != None:
            node.Upload(game.GetScore(node.lastMoved))
            node = node.parentNode

    if verbose:
        print rootnode.GetTree(0)
    else:
        pass

    #価値があるノードを最もアクセス数が多い者にする
    valueable = sorted(rootnode.childNode, key = lambda i: i.visit)[-1].move
    return valueable

# -------------------------------
## 
# @Synopsis  MC(MonteCarlo)
# 
# @Param game : ゲームの状態
# @Param times : プレイアウト回数
# @Param verbose : 冗長データ可視化
# 
# @Returns 打つ手   
# ---------------------------------
def MC(rootgame, times, verbose=False):
    #打てる手の一覧
    candidates = rootgame.GetCanMove()
    points = {}
    for i in candidates:
        #座標データはlistとして保存しているが、
        #これから点数と座標データを検索しやすいためdict型を使います
        #dict型でのkeyにはlist型を使うことができないため、座標データを
        #数値として保存する、弱点は盤面ザイズが9を超えるとバグる
        index = i[0]*10 + i[1]

        #dictのkeyを使ってvalueを初期化
        if not points.has_key(index):
            points[index]=0

        #プレイアウト
        for j in xrange(times):
            thisgame=rootgame.DeepCopy(rootgame.size)
            thisgame.DoMove(i)
            player = thisgame.lastMoved
            while thisgame.GetCanMove() != []:
                thisgame.DoMove(random.choice(thisgame.GetCanMove()))
            #結果を記録する
            points[index]+=thisgame.GetScore(player)
    #すべての試行中に一番成績がいい手を選ぶ
    get_max = max(points.iteritems(), key=operator.itemgetter(1))[0]
    #打つ手を座標に復元
    max_position = [get_max/10, get_max%10]
    if verbose:
        print "score-> " + str(points)
        print "best-> " + str(get_max)
    return max_position

# -------------------------------
## 
# @Synopsis  RandAI ランダムAI
# 
# @Param ゲーム状態
# 
# @Returns   打つ手
# ---------------------------------
def RandAI(game):
    candidate = game.GetCanMove()
    return random.choice(candidate)

# -------------------------------
## 
# @Synopsis  ScoreMax 石を多く取れるように選択AI
# 
# @Param ゲーム状態
# 
# @Returns  打つ手 
# ---------------------------------
def ScoreMax(game):
    candidate = game.GetCanMove()
    points = {}
    for i in candidate:
        thisgame=game.DeepCopy(game.size)
        thisgame.DoMove(i)
        #仮に選択した手を打ったあとの点数を計算する
        p=thisgame.GetPoint(game.lastMoved)
        if not points.has_key(p):
            points[p]=[]
        points[p].append(i)

    #最大点数の方を選択する
    max_point = max(points)
    max_candidate = points[max_point]
    return random.choice(max_candidate)

# -------------------------------
## 
# @Synopsis  Less_chance 敵の選択が狭める行動をとる
# 
# @Param ゲーム状態
# 
# @Returns   打つ手
# ---------------------------------
def Less_chance(game):
    candidates = game.GetCanMove()
    points = {}
    for i in candidates:
        thisgame = game.DeepCopy(game.size)
        thisgame.DoMove(i)
        #敵の選択子をカウントする
        c = len(thisgame.GetCanMove())
        print c
        if not points.has_key(c):
            points[c]=[]
        points[c].append(i)

    #選択可能な手を少なくする
    min_chance = min(points)
    print "min is "+str(min_chance)
    min_candidate = points[min_chance]
    return random.choice(min_candidate)

# -------------------------------
## 
# @Synopsis  ProbabilitySelect  ランダムでAIを選択するAI
# 
# @Param ゲーム状態
# 
# @Returns   打つ手
# ---------------------------------
def ProbabilitySelect(game):
    all_candidates = game.GetCanMove()
    #重み付き関数で次に使うAIを選択する
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

# -*- coding: utf-8 -*-
from math import *
import sys
import random

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
        return "+[ Move: " + str(self.move) + " NextCanMove: " + str(self.canMoveStep) + " Win: " + str(self.win) + " Visit: " + str(self.visit) + " ]"


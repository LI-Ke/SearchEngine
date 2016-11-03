# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:14:24 2016

@author: An1ta
"""
import collections

class IRmodel(object):
        
    def __init__(self, index):
        self.index = index
        self.scores = {}
        self.ranking = collections.OrderedDict()
        
    def getScores(self, query):
        raise NotImplementedError

    def getRanking(self, query):
        for doc in self.index.docs:
            if doc not in self.scores:
                self.scores[int(doc)] = 0.0
        self.ranking = sorted(self.scores.items(),  key=lambda kv: kv[1], reverse=True) #ordonner les scores dans l'ordre decroissante
        return self.ranking

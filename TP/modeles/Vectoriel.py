# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:34:58 2016

@author: An1ta


getDocWeightsForStem : {'1':3, '2':5, '3':6} frequence du mot dans chaque document

getDocWeightsForDoc : {'abc':1, 'banane':5, 'gg':3} frequence de chaque mot dans un document

query : {'a' : 1, 'b' : 2, 'c' : 3 ...}

"""
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer
from WeighterTf1 import WeighterTf1
from IRmodel import IRmodel
import numpy as np

class Vectoriel(IRmodel):
        
    def __init__(self, index, weighter, normalized = False):
        IRmodel.__init__(self, index)
        self.weighter = weighter
        self.normalized = normalized
        self.normDoc = {}
    
    def getNormDoc(self, idDoc):
        if idDoc in self.normDoc:
            return self.normDoc[idDoc]
        else:
            docWeightsForDoc = self.weighter.getDocWeightsForDoc(idDoc)
            norm = 0
            for term in docWeightsForDoc:
                norm += np.power(docWeightsForDoc[term],2)
            self.normDoc[idDoc] = np.sqrt(norm)
            return self.normDoc[idDoc]
    
    def getScores(self, query):
        weightsForQuery = self.weighter.getWeightsForQuery(query)
        sommeQuery  = 0.0    
        for stemQ in weightsForQuery: 
            sommeQuery += np.power(weightsForQuery[stemQ],2)
        normQuery = np.sqrt(sommeQuery)
        
        for term in weightsForQuery:
            if term in self.index.stems:
                docWeightsForStem = self.weighter.getDocWeightsForStem(term)
                if docWeightsForStem != None:
                    for d in docWeightsForStem :
                        score = docWeightsForStem[d] * weightsForQuery[term]
                        if self.normalized:
                            score = score / (self.getNormDoc(d) * normQuery)
                        if d in self.scores:                        
                            self.scores[d] += score
                        else:
                            self.scores[d] = score
        return self.scores
        


if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    query = {'Internat':1}
    weighter = WeighterTf1(index)
    v = Vectoriel(index,weighter, True)
    scores = v.getScores(query)
    print scores
    rang = v.getRanking(query)
    print rang
        
        
        

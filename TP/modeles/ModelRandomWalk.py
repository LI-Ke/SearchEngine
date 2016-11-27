# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 13:11:38 2016

@author: like
"""
from IRmodel import IRmodel
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTfTf import WeighterTfTf
from Vectoriel import Vectoriel
from LanguageModel import LanguageModel
from ModelOkapi import ModelOkapi
sys.path.insert(0, r'/home/like/M2/RI/TP')
from QueryParserCACM import QueryParserCACM
from TextRepresenter import PorterStemmer
from index import Index
sys.path.insert(0, r'/home/like/M2/RI/TP/liens')
from PageRank import PageRank
from HITS import HITS

class ModelRandomWalk(IRmodel):
        
    def __init__(self, index, weighter, model, randomWalk, successeurs, predecesseurs, N):
        IRmodel.__init__(self, index)
        self.weighter = weighter
        self.model = model
        self.randomWalk = randomWalk   # 1 :  PageRank    2 : HITS
        self.successeurs = successeurs
        self.predecesseurs = predecesseurs
        self.N = N
        
    def modelSousGraphe(self, query):
        docs = []
        if self.model == 1:
            m = Vectoriel(self.index,self.weighter, True)
            scores = m.getScores(query)
            ranking = m.getRanking(query)
        elif self.model == 2:
            m = LanguageModel(self.index, self.weighter)
            scores = m.lissage(query, 0.1)
            ranking = m.getRanking(query)
        else:
            m = ModelOkapi(self.index, self.weighter)
            scores = m.mesureOkapi(query, 1.5, 0.8)
            ranking = m.getRanking(query)
        
        for doc in ranking:
            docs.append(doc[0])
        
        seeds = set()
        for i in range(self.N):
            seeds.add(docs[i])
            for j in self.successeurs[docs[i]]:
                seeds.add(j)
                
        sousSuccesseurs = {}
        sousPredecesseurs = {}
        
        for doc in seeds:
            sousSuccesseurs[doc] = set()
            if doc not in sousPredecesseurs:
                sousPredecesseurs[doc] = set()
            for s in self.successeurs[doc]:
                if s in seeds:
                    sousSuccesseurs[doc].add(s)
                    if s not in sousPredecesseurs:
                        sousPredecesseurs[s] = set()
                    sousPredecesseurs[s].add(doc)
        if self.randomWalk == 1:
            rw = PageRank(0.2, 100)
        else:
            rw =  HITS(100)
        self.scores = rw.randomWalk(sousSuccesseurs, sousPredecesseurs) 
        return self.scores
        

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    #query = q.nextQuery()
    
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    succ =index.getSuccesseurs()
    pred = index.getPredecesseurs()
    weighter = WeighterTfTf(index)
        
    mrw = ModelRandomWalk(index, weighter, 1, 1, succ, pred, 20)
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    scores  = mrw.modelSousGraphe(representationQuery)
    print scores
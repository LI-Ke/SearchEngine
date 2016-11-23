# -*- coding: utf-8 -*-
"""
Created on Thu Nov  3 19:51:57 2016

@author: An1ta
"""
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer
from WeighterTfTf import WeighterTfTf
from WeighterTf1 import WeighterTf1
sys.path.insert(0, r'/home/like/M2/RI/TP/evaluation')
from QueryParserCACM import QueryParserCACM
from IRmodel import IRmodel
import numpy as np

class LanguageModel(IRmodel):
    def __init__(self,index, weighter):
        IRmodel.__init__(self, index)
        self.weighter = weighter
    
    def lissage(self,query,lmbda):
#       ii = 0
        weightsForQuery = self.weighter.getWeightsForQuery(query)
        NbMotCorpus = 0
        for doc in self.index.docs :
           tfDoc = self.index.getTfsForDoc(doc)
           for mot in tfDoc :
                NbMotCorpus += tfDoc[mot] 

        for doc in self.index.docs :
            somme = 0.0
            tfDoc = self.index.getTfsForDoc(doc)
            countText = 0
            for mot in tfDoc :
                countText += tfDoc[mot]
                
            for s in query :
                nbS = 0
                if s in self.index.stems:
                    docWeightsForStem = self.weighter.getDocWeightsForStem(s)
                    for i in docWeightsForStem :
                        nbS += docWeightsForStem[i]
                    if s in tfDoc :
                        somme += weightsForQuery[s]*(np.log(lmbda*(float(tfDoc[str(s)])/(countText*1.0))+(1-lmbda)*(float(nbS/(NbMotCorpus*1.0))))) 
                    else:
                        somme += weightsForQuery[s]*(np.log((1-lmbda)*(float(nbS/(NbMotCorpus*1.0))))) 
            self.scores[doc] = somme 
       
        return self.scores
        

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    query = q.nextQuery()
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    weighter = WeighterTf1(index)
    lm = LanguageModel(index, weighter)
    scores = lm.lissage(representationQuery,0.1)
    print scores
    rang = lm.getRanking(query)
    print rang
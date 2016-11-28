# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:10:34 2016

@author: like
"""
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
from Vectoriel import Vectoriel
from LanguageModel import LanguageModel
from ModelOkapi import ModelOkapi
sys.path.insert(0, r'/home/like/M2/RI/TP')
from QueryParserCACM import QueryParserCACM
from TextRepresenter import PorterStemmer
from index import Index
sys.path.insert(0, r'/home/like/M2/RI/TP/liens')
from Featurer import Featurer

class FeaturerModel(Featurer):
    '''
    classFeaturerModel
    '''
    def __init__(self, model ,index, weighter):
        '''
        Constructor
        '''
        self.docQueryFeature = {} #  key: idDoc  value: { query : feature} 
        self.model = model
        self.index = index
        self.weighter = weighter
        
    def getFeatures(self, idDoc, query):
        queryAsKey = tuple(sorted(query.items()))
        if (idDoc not in self.docQueryFeature) or (queryAsKey not in self.docQueryFeature[idDoc]):
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
                if doc[0] not in self.docQueryFeature:
                    self.docQueryFeature[doc[0]] = {}
                features = []
                features.append(doc[1])
                self.docQueryFeature[doc[0]][queryAsKey] = features
    
        #print self.docQueryFeature.keys   
        return self.docQueryFeature[int(idDoc)][queryAsKey]
        
if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    weighter = WeighterTf1(index)
    f = FeaturerModel(1, index, weighter)
    features = f.getFeatures('1', representationQuery)
    print features
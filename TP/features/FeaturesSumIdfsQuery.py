# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 13:47:48 2016

@author: like
"""
from Featurer import Featurer
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from index import Index
from TextRepresenter import PorterStemmer
from WeighterTf1 import WeighterTf1
sys.path.insert(0, r'/home/like/M2/RI/TP/evaluation')
from QueryParserCACM import QueryParserCACM
from IRmodel import IRmodel
import numpy as np

class FeaturesSumIdfsQuery(Featurer):
    '''
    classFeaturesSumIdfsQuery
    '''
    def __init__(self, weighter):
        '''
        Constructor
        '''
        self.sumIdfsQueryFeatures = {} #  key: dict for query   value: double list 
        self.weighter = weighter
        
    def getFeatures(self, idDoc, query):
        key = tuple(sorted(query.items()))
        if key not in self.sumIdfsQueryFeatures:
            features = []
            sumIdfs = 0.0
            nombreDocument = len(self.weighter.Index.docs)
            for term in query:
                if term in self.weighter.Index.stems:
                    sumIdfs += np.log( ( nombreDocument / (1 + len(self.weighter.Index.getTfsForStem(term))) ) )
            features.append(sumIdfs)
            self.sumIdfsQueryFeatures[key] = features
            
        return self.sumIdfsQueryFeatures[key]
        
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
    f = FeaturesSumIdfsQuery(weighter)
    features = f.getFeatures('2', representationQuery)
    print features

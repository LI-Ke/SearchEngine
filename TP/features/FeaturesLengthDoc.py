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

class FeaturesLengthDoc(Featurer):
    '''
    classFeaturesLengthDoc
    '''
    def __init__(self, weighter):
        '''
        Constructor
        '''
        self.docLengthFeature = {} #  key: idDoc  value: double list 
        self.weighter = weighter
        
    def getFeatures(self, idDoc, query): 
        if idDoc not in self.docLengthFeature:
            features = []
            countWord = 0
            tfsDoc = self.weighter.Index.getTfsForDoc(idDoc)
            for word in tfsDoc:
                countWord += tfsDoc[word]
            features.append(countWord)
            self.docLengthFeature[idDoc] = features
            
        return self.docLengthFeature[idDoc]
        
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
    f = FeaturesLengthDoc(weighter)
    features = f.getFeatures('1', representationQuery)
    print features
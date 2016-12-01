# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:25:18 2016

@author: like
"""
from Featurer import Featurer
from FeaturesLengthDoc import FeaturesLengthDoc
from FeaturesSumIdfsQuery import FeaturesSumIdfsQuery
from FeaturerModel import FeaturerModel
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
sys.path.insert(0, r'/home/like/M2/RI/TP/evaluation')
from QueryParserCACM import QueryParserCACM
import numpy as np
sys.path.insert(0, r'/home/like/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer

class FeaturerList(Featurer):
    '''
    classFeaturerList
    '''
    def __init__(self, features):
        self.features = features
        
    def getFeatures(self, idDoc, query):
        featuresList = []
        for feature in self.features:
            featuresList.append(feature.getFeatures(idDoc, query))
            
        return featuresList
        
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
    liste = []
    f = FeaturesLengthDoc(weighter)
    liste.append(f)
    f = FeaturesSumIdfsQuery(weighter)
    liste.append(f)
    f = FeaturerModel(1, index, weighter)
    liste.append(f)
    featureList = FeaturerList(liste)
    features = featureList.getFeatures('1', representationQuery)
    print features

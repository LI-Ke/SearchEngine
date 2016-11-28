# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 17:25:18 2016

@author: like
"""
from Featurer import Featurer

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
        

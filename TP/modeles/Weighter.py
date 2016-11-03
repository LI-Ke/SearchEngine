# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:34:21 2016
@author: 3402901
Created on 5 sept. 2016
"""

class Weighter(object):
    '''
    classWeighter
    '''
    def __init__(self,Index):
        '''
        Constructor
        '''
        self.Index = Index
         
    def getDocWeightsForDoc(self, idDoc): 
        raise NotImplementedError
    
    def getDocWeightsForStem(self, stem):
        raise NotImplementedError
    
    def getWeightsForQuery(self, query):
        raise NotImplementedError
  

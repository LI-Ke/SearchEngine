# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:34:21 2016
@author: 3402901
Created on 5 sept. 2016
"""
from Weighter import Weighter

class WeighterTfTf(Weighter):
    '''
    classWeighter
    '''
    def __init__(self, Index):
        '''
        Constructor
        '''
        Weighter.__init__(self, Index)
         
    def getDocWeightsForDoc(self, idDoc):
	return self.Index.getTfsForDoc(idDoc)
    
    def getDocWeightsForStem(self, stem):
	return self.Index.getTfsForStem(stem)
    
    def getWeightsForQuery(self, query):
       return query

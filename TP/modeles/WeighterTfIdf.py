# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:34:21 2016
@author: 3402901
Created on 5 sept. 2016
"""
from Weighter import Weighter
import numpy as np

class WeighterTfIdf(Weighter):
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
        nombreDocument = len(self.Index.docs)
        return {term : np.log( ( nombreDocument / (1 + len(self.Index.getTfsForStem(term))) ) ) for term in query }

            

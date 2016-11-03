# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:23:30 2016

@author: li
"""

from Weighter import Weighter
import numpy as np

class WeighterLogTfIdf(Weighter):
    '''
    classWeighter
    '''
    def __init__(self, Index):
        '''
        Constructor
        '''
        Weighter.__init__(self, Index)
         
    def getDocWeightsForDoc(self, idDoc):
        stemOcc = self.Index.getTfsForDoc(idDoc)
        return {term : (1 + np.log(stemOcc[term]) ) for term in stemOcc}
    
    def getDocWeightsForStem(self, stem):
        docOcc = self.Index.getTfsForStem(stem)
        return {doc : (1 + np.log(docOcc[doc]) ) for doc in docOcc}
    
    def getWeightsForQuery(self, query):
        nombreDocument = len(self.index.docs)
        return {term : np.log( ( nombreDocument / (1 + len(self.Index.getTfsForStem(term))) ) ) for term in query }

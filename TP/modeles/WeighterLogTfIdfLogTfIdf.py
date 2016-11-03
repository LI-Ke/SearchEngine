# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 12:33:56 2016

@author: li
"""


from Weighter import Weighter
import numpy as np

class WeighterLogTfIdfLogTfIdf(Weighter):
    '''
    classWeighter
    '''
    def __init__(self, Index):
        '''
        Constructor
        '''
        Weighter.__init__(self, Index)
         
    def getDocWeightsForDoc(self, idDoc):
        nombreDocument = len(self.Index.docs)
        stemOcc = self.Index.getTfsForDoc(idDoc)
        return {term: (1 + np.log(stemOcc[term]) * np.log( ( nombreDocument / (1 + len(self.Index.getTfsForStem(term))) ) ) ) for term in stemOcc}
    
    def getDocWeightsForStem(self, stem):
        nombreDocument = len(self.Index.docs)
        docOcc = self.Index.getTfsForStem(stem)
        return {doc : (1 + np.log(docOcc[doc]) ) * np.log( nombreDocument / (1 + len(docOcc)) ) for doc in docOcc}
    
    def getWeightsForQuery(self, query):
        nombreDocument = len(self.index.docs)
        return {term : (1 + np.log(query[term])) * np.log( ( nombreDocument / (1 + len(self.Index.getTfsForStem(term))) ) ) for term in query }
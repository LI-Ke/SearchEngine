# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:37:17 2016

@author: An1ta
"""
import sys
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer
from WeighterTfTf import WeighterTfTf
from WeighterTf1 import WeighterTf1
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP/evaluation')
from QueryParserCACM import QueryParserCACM
from IRmodel import IRmodel
import numpy as np

class ModelOkapi(IRmodel):
    def __init__(self,index, weighter):
        IRmodel.__init__(self, index)
        self.weighter = weighter        
        
    def mesureOkapi(self,query,k1,b):
        #weightsForQuery = self.weighter.getWeightsForQuery(query)
        
        NbMotCorpus = 0.
        for doc in self.index.docs :
           tfDoc = self.index.getTfsForDoc(doc)
           for mot in tfDoc :
                NbMotCorpus += tfDoc[mot]
        longueurMoyenne = NbMotCorpus/len(self.index.docs)

        LongueurDocument = {} 
        for doc in self.index.docs : 
            stems = self.index.getTfsForDoc(doc)
            length = 0
            for stem in stems :                     
                length += stems[stem]
            LongueurDocument[doc] = length
        
        N = len(self.index.docs)
        
        for doc in self.index.docs :
            somme = 0.0   
            for t in query :
                if t in self.index.stems:
                    docWeightsForStem = self.weighter.getDocWeightsForStem(t)
                    df = len(docWeightsForStem)
                    log = np.log((N - df + 0.5)/((df + 0.5) * 1.0))
                    idfp = max(0, log)
                    if doc in docWeightsForStem:
                        tf = docWeightsForStem[doc]
                    else:
                        tf = 0.0
                    numerateur = (k1+1)*tf
                    denominateur = k1*((1-b)+b*LongueurDocument[doc]/(longueurMoyenne*1.0))+tf
                    somme += idfp*numerateur/(denominateur*1.0)
            
            self.scores[doc] = somme 
          
        return self.scores  
        
if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    query = q.nextQuery()
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    weighter = WeighterTf1(index)
    mo = ModelOkapi(index, weighter)
    scores = mo.mesureOkapi(representationQuery, 1.5, 0.75)
    print scores
    rang = mo.getRanking(query)
    print rang
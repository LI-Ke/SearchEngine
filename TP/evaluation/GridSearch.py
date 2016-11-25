# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:32:17 2016

@author: 3402901
"""

import sys
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP')
from QueryParserCACM import QueryParserCACM
from TextRepresenter import PorterStemmer
from index import Index  
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
from EvalIRModel import EvalIRModel
import numpy as np

class GridSearch(object):
    def __init__(self, model, modelPrecision, queries, index, weighter):
        self.model = model  # 1: Modèle Vectoriel  2: Modèle de Langue  3: Modèle Okapi
        self.modelPrecision = modelPrecision   #  1: Precision Rappel  2: Precision Moyenne
        self.queries =queries
        self.index = index
        self.weighter = weighter
        
    def optimisation(self, listParametres):
        scoreMaxmal = 0
        meilleurParam = None
        for parametre in listParametres:
            eirm = EvalIRModel(self.queries, self.index, self.weighter, self.modelPrecision, self.model, parametre)
            mean, std = eirm.eval()
            #print mean
            if sum(mean) > scoreMaxmal:
                meilleurParam = parametre
                scoreMaxmal = sum(mean)
        
        print "Meilleur Parametre : " +  str(meilleurParam)      
        print "score : " +  str(scoreMaxmal)
    
        return meilleurParam
        
if __name__ == '__main__':
    queries = []
    textRepresenter = PorterStemmer()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    queries.append(query)
    query = q.nextQuery()
    queries.append(query)
    query = q.nextQuery()
    queries.append(query)
    
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    weighter = WeighterTf1(index)
    
    listParamsLangue = []
    for i in np.arange(0, 1.1, 0.1):
        listParamsLangue.append([i])
    
    listParamsOkapi = []
    for k in np.arange(1.0, 2.1, 0.1):
        for b in np.arange(0.7, 0.8, 0.01):
            listParamsOkapi.append([k,b])
         
    #print  listParamsOkapi
    #gs = GridSearch(2, 2, queries, index, weighter)
    #mp = gs.optimisation(listParamsLangue) # Modele de Langue lambde = 0.1
    gs = GridSearch(3, 2, queries, index, weighter)
    mp = gs.optimisation(listParamsOkapi)  # Modele Okapi k1 = 1.5  b = 0.8
    print mp

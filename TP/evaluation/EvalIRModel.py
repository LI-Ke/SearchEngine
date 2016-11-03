# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:58:09 2016

@author: like
"""
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
import numpy as np
from IRList import IRList
from QueryParserCACM import QueryParserCACM
from TextRepresenter import PorterStemmer
from index import Index  
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
from Vectoriel import Vectoriel
from PrecisionRappel import PrecisionRappel

class EvalIRModel(object):
    def __init__(self, queries, index, weighter):
        self.queries = queries
        self.index = index
        self.weighter = weighter
        self.mean = []
        self.std = []

    def eval(self):
        textRepresenter = PorterStemmer()
        prelist = []
        for idQuery in range(len(self.queries)):
            query = self.queries[idQuery]
            if len(query.relevants) != 0:
                stems = textRepresenter.getTextRepresentation(query.text)
                v = Vectoriel(self.index,self.weighter, True)
                scores = v.getScores(stems)
                ranking = v.getRanking(stems)
                irlist = IRList(query,ranking)
                mesure = PrecisionRappel()
                prelist.append(mesure.eval(irlist))
        
        print prelist
        #Calculer les moyenne
        cellule = prelist[0]
        lenCel = len(cellule)
        for i in range(lenCel):
            cel = 0.0
            for j in range(len(prelist)):
                cel += prelist[j][i]
            self.mean.append(cel/len(prelist))     
				

        #Calculer les ecart-types
        for i in range(lenCel):
            ecart = 0.0
            for j in range(len(prelist)):
                ecart += np.power(prelist[j][i]-self.mean[j],2)
            self.std.append(np.sqrt(ecart))
        return self.mean, self.std

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
    
    eirm = EvalIRModel(queries,index,weighter)
    mean, std = eirm.eval()
    print mean
    print std
    

# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 11:55:40 2016

@author: An1ta
"""
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')

from EvalMeasure import EvalMeasure
#import collections
from IRList import IRList
from QueryParserCACM import QueryParserCACM
from index import Index       
from TextRepresenter import PorterStemmer
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
from Vectoriel import Vectoriel

class PrecisionMoyenne(EvalMeasure):
    def __init__(self):
        self.precision = 0.0
        self.preMoy = []
    
    
    def eval(self, IRList):
        lengthDoc = len(IRList.documentScore)
        nbr_relevants = len(IRList.query.relevants)
        nbDocPertinent = 0.0
        for i in range(lengthDoc) :
            if IRList.documentScore[i][0] in IRList.query.relevants :
                nbDocPertinent += 1.
                pre = nbDocPertinent*1.0/(i+1)
                self.precision += pre
        self.preMoy.append(self.precision/nbr_relevants)
        
        return self.preMoy
 
 

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    weighter = WeighterTf1(index)
    v = Vectoriel(index,weighter, True)
    scores = v.getScores(representationQuery)
    rang = v.getRanking(representationQuery)                  
    irlist = IRList(query,rang)
    pm = PrecisionMoyenne()
    preMoy = pm.eval(irlist)
    print preMoy

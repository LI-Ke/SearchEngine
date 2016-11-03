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
import numpy as np
import matplotlib.pyplot as plt

class PrecisionRappel(EvalMeasure):
    def __init__(self):
        self.precision = []
        self.rappel = []
        #self.preRap = collections.OrderedDict()
        self.preRap = []
    #pour chaque document, parcours tout de rappel, si rappel > niveau, cherche le max de prediction a partir de ce document, sinon, looping rappel 
    def eval(self, IRList, nbLevels=10):
        lengthDoc = len(IRList.documentScore)
        nbDocPertinent = 0.
        niveau = 1./nbLevels
        #precisiontmp = {}
        for i in range(lengthDoc) :
            if IRList.documentScore[i][0] in IRList.query.relevants :
                nbDocPertinent += 1.
            self.precision.append(nbDocPertinent/(i+1))
            self.rappel.append(nbDocPertinent/len(IRList.query.relevants))
        #self.precision = sorted(precisiontmp.items(),  key=lambda kv: kv[1], reverse=True) #ordonner les items de precisontmp decroissant
        k = 0
        while niveau <= 1 :
            if(self.rappel[k]>=niveau):
                self.preRap.append(np.max(self.precision[k:]))
                niveau += 1./nbLevels
            else :
                k+=1
        
        return self.preRap
 
 

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    representationQuery = textRepresenter.getTextRepresentation(query.text)
    print representationQuery
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    weighter = WeighterTf1(index)
    v = Vectoriel(index,weighter, True)
    scores = v.getScores(representationQuery)
    rang = v.getRanking(representationQuery)                  
    irlist = IRList(query,rang)
    rp = PrecisionRappel()
    preRap = rp.eval(irlist,10)
    print preRap

    """
    x = []
    y = []
    for  i in range(1,11,1):
        j =i/10.
        y.append(preRap[i-1])
        x.append(j)
    plt.plot(x, y, linewidth=2.0)
    plt.xlabel("Rappel")
    plt.ylabel("Precision")
    plt.show()
    """
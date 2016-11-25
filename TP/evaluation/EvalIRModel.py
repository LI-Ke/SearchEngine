# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 16:58:09 2016

@author: like
"""
import sys
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP')
import numpy as np
from IRList import IRList
from QueryParserCACM import QueryParserCACM
from TextRepresenter import PorterStemmer
from index import Index  
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
from Vectoriel import Vectoriel
from LanguageModel import LanguageModel
from ModelOkapi import ModelOkapi
from PrecisionRappel import PrecisionRappel
from PrecisionMoyenne import PrecisionMoyenne

class EvalIRModel(object):
    def __init__(self, queries, index, weighter, modelPrecision, model, params=[1.5, 0.75]):
        self.queries = queries
        self.index = index
        self.weighter = weighter
        self.mean = []
        self.std = []
        self.modelPrecision = modelPrecision  #  1: Precision Rappel  2: Precision Moyenne
        self.model = model   # 1: Modèle Vectoriel  2: Modèle de Langue  3: Modèle Okapi
        self.params = params

    def eval(self):
        textRepresenter = PorterStemmer()
        prelist = []
        for idQuery in range(len(self.queries)):
            query = self.queries[idQuery]
            if len(query.relevants) != 0:
                stems = textRepresenter.getTextRepresentation(query.text)
                if self.model == 1:
                    m = Vectoriel(self.index,self.weighter, True)
                    scores = m.getScores(stems)
                    ranking = m.getRanking(stems)
                elif self.model == 2:
                    m = LanguageModel(self.index, self.weighter)
                    scores = m.lissage(stems,self.params[0])
                    ranking = m.getRanking(query)
                else:
                    m = ModelOkapi(self.index, self.weighter)
                    scores = m.mesureOkapi(stems, self.params[0], self.params[1])
                    ranking = m.getRanking(query)
                
                irlist = IRList(query,ranking)
                if self.modelPrecision == 1:
                    mesure = PrecisionRappel()
                else:
                    mesure = PrecisionMoyenne()
                prelist.append(mesure.eval(irlist))
        
        #print prelist
        #Calculer les moyenne
        cellule = prelist[0]
        lenCel = len(cellule)
        for i in range(lenCel):
            cel = 0.0
            for j in range(len(prelist)):
                cel += prelist[j][i]
            self.mean.append(cel/len(prelist))     
				
        #Calculer les ecart-types
        if lenCel > 1:
            for i in range(lenCel):
                ecart = 0.0
                for j in range(len(prelist)):
                    ecart += np.power(prelist[j][i]-self.mean[j],2)
                self.std.append(np.sqrt(ecart))
        else:
            ecart = 0.0
            for j in range(len(prelist)):
                ecart += np.power(prelist[j][i]-self.mean[0],2)
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
    
    eirm = EvalIRModel(queries,index,weighter, 2, 2, [0.0]) 
    mean, std = eirm.eval()
    print mean
    print std

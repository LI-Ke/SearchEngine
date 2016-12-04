# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:35:09 2016

@author: like
"""

import numpy as np
from MetaModel import MetaModel
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from TextRepresenter import PorterStemmer

class MetaModelLinear(MetaModel):
    '''
    classMetaModelLinear
    '''
    def __init__(self, weighter, featurer, tmax, alpha, sigma):
        self.weighter = weighter
        self.featurer = featurer
        self.tmax = tmax
        self.alpha = alpha
        self.sigma = sigma
        self.weighters = []
        nbrFeature = 0
        for feature in featurer:
            nbrFeature += 0
        for i in range (nbrFeature):
            self.weighters.append(0.0)
        
    def optimisation(self, queries):
        loss = 0.0
        textRepresenter = PorterStemmer()
        for t in range(self.tmax):
            idQuery = np.random.randint(0,len(queries))
            query = queries[idQuery]
            if len(query.relevants)!=0 and len(query.relevants)!=len(self.weighter.Index.docs) :
                docPert = np.random.choice(query.relevants.keys())
                docNonPert = np.random.choice(self.weighter.Index.docs.keys())
                while docNonPert in query.relevants.keys() :
                    docNonPert = np.random.choice(self.weighter.Index.docs.keys())
                stems = textRepresenter.getTextRepresentation(query.text)
                featuresPert = self.featurer.getFeatuers(docPert, stems)
                featuresNonPert = self.featurer.getFeatuers(docNonPert, stems)
                scorePert = 0.0
                scoreNonPert = 0.0
                for i in range(len(self.weighters)):
                    scorePert += self.weighters[i] * featuresPert[i]
                    scoreNonPert += self.weighters[i] * featuresNonPert[i]
                if (1 - scorePert + scoreNonPert > 0):
                    for i in range(len(self.weighters)):
                        self.weighters[i] += self.alpha*(featuresPert[i] - featuresNonPert[i])
                normWeighter = 0.0
                for i in range(len(self.weighters)):
                    self.weighters[i] *= (1 - 2 * self.alpha * self.sigma)
                    normWeighter += np.power(self.weighters[i], 2)
                loss += np.max(0, 1 - scorePert + scoreNonPert) + self.alpha * normWeighter
                            
    
    def getScores(self, query):
        for idDoc in self.weighter.Index.docs:
            features = self.featurer.getFeatuers(idDoc, query)
            score = 0.0
            for i in range(len(self.weighters)):
                score += self.weighters[i] * features[i]
            self.score[idDoc] = score
            
        
        
        
        
        
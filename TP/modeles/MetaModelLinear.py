# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:35:09 2016

@author: like
"""

import numpy as np
import time
from MetaModel import MetaModel
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from TextRepresenter import PorterStemmer
from index import Index
sys.path.insert(0, r'/home/like/M2/RI/TP/evaluation')
from QueryParserCACM import QueryParserCACM
import EvalIRModel 
sys.path.insert(0, r'/home/like/M2/RI/TP/modeles')
from WeighterTf1 import WeighterTf1
sys.path.insert(0, r'/home/like/M2/RI/TP/features')
from FeaturesLengthDoc import FeaturesLengthDoc
from FeaturesSumIdfsQuery import FeaturesSumIdfsQuery
from FeaturerModel import FeaturerModel
from FeaturerList import FeaturerList


class MetaModelLinear(MetaModel):
    '''
    classMetaModelLinear
    '''
    def __init__(self, index, weighter, featurer, tmax, alpha, sigma):
        MetaModel.__init__(self, index, featurer)
        self.weighter = weighter
        self.featurerList = featurer.features
        self.featurer = featurer
        self.tmax = tmax
        self.alpha = alpha
        self.sigma = sigma
        self.weighters = []
        nbrFeature = 0
        for feature in self.featurerList:
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
                featuresPert = self.featurer.getFeatures(docPert, stems)
                featuresNonPert = self.featurer.getFeatures(docNonPert, stems)
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
                loss += max(0, 1 - scorePert + scoreNonPert) + self.alpha * normWeighter
                            
    
    def getScores(self, query):
        for idDoc in self.weighter.Index.docs:
            features = self.featurer.getFeatures(idDoc, query)
            score = 0.0
            for i in range(len(self.weighters)):
                score += self.weighters[i] * features[i]
            self.scores[idDoc] = score
        
        return self.scores
            
        
if __name__ == '__main__':
    start_time = time.time()

    textRepresenter = PorterStemmer()
    queries = []
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    queries.append(query)
    query = q.nextQuery()
    queries.append(query)
    query = q.nextQuery()
    queries.append(query)
    #representationQuery = textRepresenter.getTextRepresentation(query.text)
    weighter = WeighterTf1(index)
    liste = []
    f = FeaturesLengthDoc(weighter)
    liste.append(f)
    f = FeaturesSumIdfsQuery(weighter)
    liste.append(f)
    f = FeaturerModel(1, index, weighter)
    liste.append(f)
    featureList = FeaturerList(liste)
    #features = featureList.getFeatures('1', representationQuery)        
    eirm = EvalIRModel.EvalIRModel(queries, index, weighter, 2, 4, [20, 0.001, 0.1], featureList) 
    mean, std = eirm.eval()
    print mean
    print std
    print("--- %s seconds ---" % (time.time() - start_time))
    

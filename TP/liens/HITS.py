# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:14:54 2016

@author: like
"""
import numpy as np
from RandomWalk import RandomWalk
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer

class HITS(RandomWalk):
    '''
    classHITS
    '''
    def __init__(self, nbrIter):
        '''
        Constructor
        '''
        self.nbrIter = nbrIter
        self.a = {}
        self.h = {}
        
    def randomWalk(self, successeurs, predecesseurs):
        for neud in predecesseurs:
            self.a[neud] = 1.0
            self.h[neud] = 1.0
        
        for t in range(self.nbrIter):
            hub = 0
            aut = 0
            for i in predecesseurs:
                somme = 0
                for j in predecesseurs[i]:
                    somme += self.h[j]
                self.a[i] = somme
                hub += np.power(somme, 2)
                somme = 0
                for j in successeurs[i]:
                    somme += self.a[j]
                self.h[i] = somme
                aut += np.power(somme, 2)
            hubNorm = np.sqrt(hub)
            autNorm = np.sqrt(aut)
            
            for neud in predecesseurs:
                self.a[neud] = self.a[neud]/(hubNorm*1.0)
                self.h[neud] = self.h[neud]/(autNorm*1.0)
                
        return self.a
        

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    
    hits = HITS(100)
    succ =index.getSuccesseurs()
    pred = index.getPredecesseurs()
    authority = hits.randomWalk(succ, pred)
    print authority
    print max(authority, key=authority.get)
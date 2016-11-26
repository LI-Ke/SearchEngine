# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 17:36:15 2016

@author: 3402901
"""
from RandomWalk import RandomWalk
import sys
sys.path.insert(0, r'/users/Etu1/3402901/M2/RI/TP')
from index import Index
from TextRepresenter import PorterStemmer

class PageRank(RandomWalk):
    '''
    classWeighter
    '''
    def __init__(self, d, nbrIter):
        '''
        Constructor
        '''
        self.d = d
        self.nbrIter = nbrIter
        self.mu = {}
         
    def randomWalk(self, successeurs, predecesseurs):
        N = len(successeurs)
        
        for page in successeurs:
            self.mu[page] = 1/(N*1.0)
        
        for t in range(self.nbrIter):
            for i in predecesseurs:
                somme = 0.0
                for j in predecesseurs[i]:
                    somme += self.mu[i] / (len(successeurs[j])*1.0)
                somme *= self.d
                somme += (1-self.d)/(N*1.0)
                self.mu[i] = somme
        
        return self.mu
        
        
        
if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "../cacm/cacm.txt"
    index = Index("../document",source,textRepresenter)
    index.indexation()
    
    pr = PageRank(0.2, 10)
    succ =index.getSuccesseurs()
    pred = index.getPredecesseurs()
    mu = pr.randomWalk(succ, pred)
    print mu

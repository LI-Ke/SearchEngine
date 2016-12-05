# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:06:53 2016

@author: like
"""
from IRmodel import IRmodel

class MetaModel(IRmodel):
    '''
    classMetaModel
    '''
    def __init__(self, index, FeaturersList):
        IRmodel.__init__(self, index)
        self.FeaturersList = FeaturersList

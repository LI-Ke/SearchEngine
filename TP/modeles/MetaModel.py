# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 12:06:53 2016

@author: like
"""
from IRModel import IRModel

class MetaModel(IRModel):
    '''
    classMetaModel
    '''
    def __init__(self, FeaturersList):
        self.FeaturersList = FeaturersList
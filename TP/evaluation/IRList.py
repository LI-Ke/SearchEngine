# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 23:05:28 2016

@author: li
"""

class IRList(object):
    def __init__(self, query, documentScore):
        self.query = query
        self.documentScore = documentScore
        

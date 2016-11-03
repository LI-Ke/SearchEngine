# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 17:55:40 2016

@author: li
"""


class Query(object):
    
    def __init__(self, idQuery, text):
        self.idQuery = idQuery
        self.text = text
        self.relevants = {}
        
    def putRelevants(self, idDoc, relevant):
        self.relevants[idDoc] = relevant
    
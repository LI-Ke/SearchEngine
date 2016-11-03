# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 17:47:53 2016

@author: li
"""
import collections
import sys
sys.path.insert(0, r'/home/like/M2/RI/TP')
from ParserCACM import ParserCACM
from Query import Query
from QueryParser import QueryParser

class QueryParserCACM(QueryParser):
    
    def __init__(self):
        self.queries = collections.OrderedDict()
        self.indicator = 1
        self.lastQuery = 0
        
    def initFile(self, fileQuery, fileJugement):
        parser = ParserCACM()
        parser.initFile(fileQuery)
        queryDoc = parser.nextDocument()
        while ( queryDoc ):
            self.queries[queryDoc.identifier] = Query(queryDoc.identifier, queryDoc.text)
            queryDoc = parser.nextDocument()
        
        f = open(fileJugement,"rb")
        line = f.readline()
        while( line ):
            strings = line.split(" ")
            idQuery = str(int(strings[0]))
            idDoc = str(int(strings[1]))
            if len(strings) == 4:
                thirdCol = str(strings[2])
                forthCol = str(strings[3])
            else:
                thirdCol = str(strings[3])
                forthCol = strings[4].split("\n")[0]
            line = f.readline()
            self.queries[idQuery].putRelevants(idDoc, (thirdCol, forthCol))
               
        self.lastQuery = self.queries.keys()[-1]

    def nextQuery(self):
        if int(self.indicator) <= int(self.lastQuery):
            query = self.queries[str(self.indicator)]
            nextKey =  self.queries.items()[self.queries.keys().index(str(self.indicator)) + 1][0]
            self.indicator = nextKey
            return query
        else:
            return None
        

if __name__ == '__main__':      
    q = QueryParserCACM()
    q.initFile("../cacm/cacm.qry","../cacm/cacm.rel")
    query = q.nextQuery()
    print query.idQuery,query.text,query.relevants
    query = q.nextQuery()
    print query.idQuery,query.text,query.relevants
    query = q.nextQuery()
    print query.idQuery,query.text,query.relevants
    #print query


# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:34:21 2016
@author: 3402901
Created on 5 sept. 2016
"""
"""
index:
    "1" : ("cat":3);("chien",2);

index inversé:
    "cat" : (3:1),(2,4);
    "chien" : (1:2)
"""
from ParserCACM import ParserCACM
from TextRepresenter import PorterStemmer
import copy
import pickle
import os.path


class Index(object):
    '''
    classIndex
    '''
    def __init__(self,name,fichier,textRepresenter):
        '''
        Constructor
        '''
        self.name = name
        self.fichier = fichier
        self.docs = {}
        self.stems = {}
        self.docFrom = {}
        self.parser = ParserCACM()
        self.parser.initFile(self.fichier)
        self.textRepresenter = textRepresenter
        
        self.successuers = {}
        self.predecesseurs = {}
         
        
    def indexation(self):
        if os.path.exists('/users/Etu1/3402901/M2/RI/TP/docs.pickle'):
            with open('/users/Etu1/3402901/M2/RI/TP/docs.pickle', 'rb') as docsWriter:
                self.docs = pickle.load(docsWriter)
            with open('/users/Etu1/3402901/M2/RI/TP/docFrom.pickle', 'rb') as docFromWriter:
                self.docFrom = pickle.load(docFromWriter)
            with open('/users/Etu1/3402901/M2/RI/TP/stems.pickle', 'rb') as stemsWriter:
                self.stems = pickle.load(stemsWriter)
            with open('/users/Etu1/3402901/M2/RI/TP/successeurs.pickle', 'rb') as successeurWriter:
                self.successuers = pickle.load(successeurWriter)
            with open('/users/Etu1/3402901/M2/RI/TP/predecesseurs.pickle', 'rb') as predecesseurWriter:
                self.predecesseurs = pickle.load(predecesseurWriter)
        
        else:
            f = open(self.name+"_index", 'w+')
            doc = self.parser.nextDocument()
            position = 0
            stemsPropriete = {}
            while doc:
                representationDoc = self.textRepresenter.getTextRepresentation(doc.getText())
                rep = {doc.getId():representationDoc}
                string = str(rep) + "\n"
                self.docs[doc.getId()] = {'position':position,'longueur':len(string)}
                position += len(string)
                f.write(string)
                #table de hashage contenant pour chaque document son fichier source ainsi que sa position et sa longueur en octets dans celui-ci.
                self.docFrom[doc.getId()] = doc.get("from").split(';')
                #on stocke les infos utiles par rapport à un stem pour constuire un undex inversé
                for key, value in representationDoc.iteritems():
                    propriete = {
                        'nbr_occurence':1, # nombre de document qui contient le stem
                        'longueurValeur':len(str(value)),
                        'longueurId':len(str(doc.getId())),
                    }
                    if key in stemsPropriete:
                        stemsPropriete[key]['nbr_occurence'] += 1
                        stemsPropriete[key]['longueurValeur'] += propriete['longueurValeur']
                        stemsPropriete[key]['longueurId'] += propriete['longueurId']
                    else:
                        stemsPropriete[key] = propriete
                
                doc = self.parser.nextDocument()   
            f.close() 
            with open('/users/Etu1/3402901/M2/RI/TP/docs.pickle', 'wb') as docsWriter:
                pickle.dump(self.docs, docsWriter)
                 
            with open('/users/Etu1/3402901/M2/RI/TP/docFrom.pickle', 'wb') as docFromWriter:
                pickle.dump(self.docFrom, docFromWriter)
            
            pos = 0
            for key, value in stemsPropriete.iteritems():
                longueur = len(key) + stemsPropriete[key]['longueurValeur'] + stemsPropriete[key]['longueurId'] + (stemsPropriete[key]['nbr_occurence']+1)*3 + (stemsPropriete[key]['nbr_occurence']-1) + 4
                self.stems[key] = [pos, longueur] 
                pos += longueur + 1      
            
            with open('/users/Etu1/3402901/M2/RI/TP/stems.pickle', 'wb') as stemsWriter:
                pickle.dump(self.stems, stemsWriter)   
            
            #Index inversé
            f = open(self.name+"_inverted", 'w+')
            self.parser.initFile(self.fichier) # reparser
            doc = self.parser.nextDocument()
            tmpStems = copy.deepcopy(self.stems)
            while doc :
                representationDoc = self.textRepresenter.getTextRepresentation(doc.getText())
                for key, value in representationDoc.iteritems():
                    # si on n'est pas au début de la première ligne
                    if tmpStems[key][0] != 0:
                        f.seek(tmpStems[key][0]-1)
                        char = f.read(1)
                        if char == "," :
                            string = "'" + doc.getId() + "':" + str(value) + "}}"
                            if ( len(string) != tmpStems[key][1] ):
                                string = "'" + doc.getId() + "':" + str(value) + ","
                                f.seek(tmpStems[key][0]) 
                                f.write(string)
                                tmpStems[key][0] += len(string)
                                tmpStems[key][1] -= len(string)
                            else :
                                f.seek(tmpStems[key][0]) 
                                f.write(string+"\n")
                                tmpStems[key][0] += len(string)
                                tmpStems[key][1] -= len(string)
                        else:
                            string = "{'" + key + "':{'" + doc.getId() + "':" + str(value) + "}}"
                            if ( len(string) == tmpStems[key][1] ):
                                f.seek(tmpStems[key][0])
                                f.write(string+"\n")
                                tmpStems[key][0] += len(string)
                                tmpStems[key][1] -= len(string)
                            else:
                                string = "{'" + key + "':{'" + doc.getId() + "':" + str(value) + ","
                                f.seek(tmpStems[key][0])
                                f.write(string)
                                tmpStems[key][0] += len(string)
                                tmpStems[key][1] -= len(string)                    
                    
                    # si on est au début de la première ligne
                    else:
                        string = "{'" + key + "':{'" + doc.getId() + "':" + str(value) + "}}"
                        if ( len(string) == tmpStems[key][1] ):
                            f.seek(tmpStems[key][0]) 
                            f.write(string+"\n")
                            tmpStems[key][0] += len(string)
                            tmpStems[key][1] -= len(string)
                        else:
                            string = "{'" + key + "':{'" + doc.getId() + "':" + str(value) + ","
                            f.seek(tmpStems[key][0]) 
                            f.write(string)
                            tmpStems[key][0] += len(string)
                            tmpStems[key][1] -= len(string)
                    
                self.successuers[doc.getId()] = set()
                if doc.getId() not in self.predecesseurs:
                    self.predecesseurs[doc.getId()] = set()
                if doc.get('links') != '':
                    for suc in doc.get('links').split(";"):
                        if suc != '':
                            self.successuers[doc.getId()].add(suc)
                            if suc not in self.predecesseurs:
                                self.predecesseurs[suc] = set()
                            self.predecesseurs[suc].add(doc.getId())
                
                doc = self.parser.nextDocument()         
            with open('/users/Etu1/3402901/M2/RI/TP/successeurs.pickle', 'wb') as successeurWriter:
                pickle.dump(self.successuers, successeurWriter)
            with open('/users/Etu1/3402901/M2/RI/TP/predecesseurs.pickle', 'wb') as predecesseurWriter:
                pickle.dump(self.predecesseurs, predecesseurWriter)
            f.close()
        
    
    def getTfsForDoc(self,docId):
        """
        Retourne la représentation (stem-tf) d'un document à partir de l'index.
        """
        f = open(self.name+"_index", 'r+')
        f.seek(self.docs[docId]['position'])
        line = f.readline()
        f.close()
        representationDoc = eval(line) # convertir la ligne en un dictionaire
        return representationDoc[docId]
            
    def getTfsForStem(self,stem):
        """
        Retourne la représentation (doc-tf) d'un stem à partir de l'index inversé.
        """
        f = open(self.name+"_inverted", 'r+')
        f.seek(self.stems[stem][0])
        line = f.readline()
        f.close()
        representationStem = eval(line) # convertir la ligne en un dictionaire
        return representationStem[stem]

    def getStrDoc(self,docId):
        """
        retourne la chaîne de caractères dont est issu un document donné dans le fichier source
        """
        f = open(self.fichier, 'r+')
        f.seek(int(self.docFrom[docId][1]))
        contenu = f.read(int(self.docFrom[docId][2]))
        f.close()
        return contenu
        
    def getSuccesseurs(self):
        return self.successuers
        
    def getPredecesseurs(self):
        return self.predecesseurs

if __name__ == '__main__':
    textRepresenter = PorterStemmer()
    source = "cacm/cacm.txt"
    index = Index("document",source,textRepresenter)
    index.indexation()
    print index.getTfsForDoc("20")
    print index.getTfsForStem("PRISM")
    print index.getStrDoc("1")
    print index.getSuccesseurs()['1']
    print index.getPredecesseurs()['100']


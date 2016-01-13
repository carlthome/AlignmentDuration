# -*- coding: utf-8 -*-

'''



@author: joro
'''


import codecs
import os
import sys
import json
from Section import Section

parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__) ), os.path.pardir)) 
pathUtils = os.path.join(parentDir, 'utilsLyrics') 

# utils_ = imp.load_source('Utils', pathUtils  )

sys.path.append(pathUtils )

from Utilz import  loadTextFile


'''
Parses lyrics from symbTr v 1.0. Sections from tsv file
a list of syllables is parsed. 
Base class. DO not instantiate

TODO: take only section names from tsv file. parse sections from symbTr double spaces 
'''
class _SymbTrParserBase(object):
    
    def __init__(self, pathToSymbTrFile,  sectionMetadataFileURI):
        '''
        Constructor
        '''
        # list of note number and syllables
        self.listSyllables =[]
        self._loadSyllables( pathToSymbTrFile)


        #  list of objects of Section class
        self.sections = []
        self._loadSectionBoundaries(sectionMetadataFileURI)
        
    
    def  _loadSyllables(self, pathToSymbTrFile):
        raise NotImplementedError("a parsing function must be implemented")

   ##################################################################################

    def _loadSectionBoundaries(self, sectionMetadataFileURI):
            if not os.path.isfile(sectionMetadataFileURI):
                sys.exit("no file {}".format(sectionMetadataFileURI))
            
            ext = os.path.splitext(os.path.basename(sectionMetadataFileURI))[1] 
            if ext == '.tsv':
                allLines = loadTextFile(sectionMetadataFileURI)
    
                for line in allLines[1:]:
                    #  triples of sectin name, start note number, end note number 
                    tokens = line.strip().split("\t")
                    if not len(tokens)==3:
                        sys.exit("tokens in line {} from file {} are not 3. make sure /t  are used".format( line, sectionMetadataFileURI))
                        
                    tmpTriplet = tokens[0], int(tokens[1]), int(tokens[2]) 
                    self.sections.append(tmpTriplet)
            ######################
            elif ext == '.json':
                
                b = open (sectionMetadataFileURI)
                scoreAnno = json.load(b)
                b.close()
                scoreSectionAnnos = scoreAnno['sections']
                
                for section in scoreSectionAnnos:
                    sectionNew = Section(section['name'],  int(section['startNote']), int(section['endNote']), section['melodicStructure'], section['lyricStructure']) 
                    
                    self.sections.append(sectionNew)
    
    def syllables2Lyrics(self):
        '''
        put lyrics into self.sectionLyrics = []
        '''
        raise NotImplementedError("a syllable2Lyrics function must be implemented")
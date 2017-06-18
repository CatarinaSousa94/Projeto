# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 10:43:36 2017

@author: Catar
"""

from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
import argparse
import webbrowser
import time
import json
import os
import unittest
import urllib2
import pycurl
import multiprocessing 
import shutil
import gzip 

class BaseSpace_fastqReadCounter:
    def __init__(self, workdir, client_key, client_secret, accessToken, AppSessionId=''):
        self.workdir=workdir 
        self.BaseSpaceUrl= 'https://api.basespace.illumina.com/'
        self.version= 'v1pre3'
        self.client_key=client_key             
        self.client_secret=client_secret         
        self.AppSessionId=AppSessionId
        self.accessToken=accessToken  
        self.myAPI= BaseSpaceAPI(self.client_key, self.client_secret, self.BaseSpaceUrl, self.version, self.AppSessionId, AccessToken=self.accessToken)

    def getUser(self):
        user= self.myAPI.getUserById('current')
        #print user.Email
        return user
    
    def getProjects(self):
        myProjects = self.getUser().getProjects(self.myAPI)
        return myProjects
    
    def getRuns(self):
        runs = self.getUser().getRuns(self.myAPI)
        return runs
    
    def getResultsProject(self, projectId):
        return self.myAPI.getProjectById(projectId).getAppResults(self.myAPI)
    
    def getSamplesProject(self, projectId):
        return self.myAPI.getProjectById(projectId).getSamples(self.myAPI)
    
    def getFilesFromSample(self, sampleId):   
        return self.myAPI.getFilesBySample(sampleId)
    
    def processFile(self,file, sampleId, projectId, appResultName, appResultDescricao, myDir=""): 
        #cada sample tem no max 2 ficheiros 
        file.downloadFile(self.myAPI, self.workdir)
        f= gzip.open(self.workdir+os.sep+str(file), "r") 
        file_content=f.readlines()
        f.close()
        tam=len(file_content)/4 ##### nr de reads 
        resultFile=self.workdir+os.sep+str(file)+'_Result.txt'
        f1 = open(resultFile,'w')
        f1.write("O nr de reads é: " +str(tam)+"\n")
        f1.close()
        p= self.myAPI.getProjectById(projectId)
        appResults = p.createAppResult(self.myAPI,appResultName,appResultDescricao, appSessionId=self.AppSessionId)
        appResults.uploadFile(self.myAPI, resultFile, str(file)+'_Result.txt', myDir, 'text/plain')
    
def test():
    workdir="C:\Users\Catar\Desktop\PROJECTX"
    BaseSpaceUrl          = 'https://api.basespace.illumina.com/'
    version         = 'v1pre3'
    client_key                 = "9d8850504c174951aa2cf1842e1f251f"
    client_secret              = "73c325bbcf174b90b8c4eb7d34508531"
    AppSessionId           =  ""
    accessToken                = "62943acc7d964d2389c9d887f5736806"
    
    app= BaseSpace_fastqReadCounter(workdir, client_key, client_secret, accessToken,AppSessionId)
    print(app.getUser())
    #print(app.getProjects())
    for project in app.getProjects():
        print str(project.Id)+"->"+str(project.Name)
    print(app.getRuns())
    projectId=str(input('Introduza o id do projeto'))
    print(app.getResultsProject(projectId))
    #print(app.getSamplesProject(projectId))
    for sample in app.getSamplesProject(projectId):
        print str(sample.Id)+"->"+str(sample.Name)
    sampleId=str(input('Introduza o id da sample'))
   # print(app.getFilesFromSample(sampleId))
    dic={}
    for file in app.getFilesFromSample(sampleId):
        dic[str(file.Id)]=file
        print str(file.Id)+"->"+str(file.Name)
    fileId=str(input('Introduza o id do file'))
    appResultName=str(raw_input('Introduza o nome do app result:'))
    app.processFile(dic[fileId],sampleId, projectId, appResultName, "Numero de reads de um ficheiro Fastq")
'''  
def test2():
    workdir="C:\Users\Catar\Desktop\PROJECTX"
    BaseSpaceUrl          = 'https://api.basespace.illumina.com/'
    version         = 'v1pre3'
    client_key                 = "9f516254aee74132baebdf2e4418ded9"
    client_secret              = "06404ae6649849ee9941c2dc7ec871b7"
    AppSessionId           =  ""
    accessToken                = "04ad95f64d04490798cac25c24243204"
    
    app= BaseSpace_fastqReadCounter(workdir, client_key, client_secret, accessToken,AppSessionId)
    print(app.getUser())
    #print(app.getProjects())
    for project in app.getProjects():
        print str(project.Id)+"->"+str(project.Name)
    print(app.getRuns())
    projectId=str(input('Introduza o id do projeto'))
    print(app.getResultsProject(projectId))
    #print(app.getSamplesProject(projectId))
    for sample in app.getSamplesProject(projectId):
        print str(sample.Id)+"->"+str(sample.Name)
    sampleId=str(input('Introduza o id da sample'))
   # print(app.getFilesFromSample(sampleId))
    dic={}
    for file in app.getFilesFromSample(sampleId):
        dic[str(file.Id)]=file
        print str(file.Id)+"->"+str(file.Name)
    fileId=str(input('Introduza o id do file'))
    appResultName=str(raw_input('Introduza o nome do app result:'))
    app.processFile(dic[fileId],sampleId, projectId, appResultName, "Numero de reads de um ficheiro Fastq")
    
'''

test1()
        
    
        
        
    
    
            

        
    
    
    
    
    

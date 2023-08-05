# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 19:01:14 2022

@author: Masume, Deepak
"""

# loading all the packages
import os
import pandas as pd
import re
import preprocessor as p
import numpy

from sentence_transformers import SentenceTransformer

#%%
# defining the individual functions
def load_model(compute):
    """
    Function to utilize gpu if called
    """
    if compute == 'cuda':
        embedder = SentenceTransformer('all-MiniLM-L6-v2', device = compute)
    else:
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    return embedder

def cosinesim(v1, v2):
    """
    Function to find cosine similarity
    """
    return numpy.dot(v1, v2)/(numpy.linalg.norm(v1)* numpy.linalg.norm(v2))

def clean_text(text_list):
    """
    custum function to clean the dataset (combining tweet_preprocessor and reguar expression)
    """
    #set up punctuations we want to be replaced
    REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\|)|(\()|(\))|(\[)|(\])|(\%)|(\$)|(\>)|(\<)|(\{)|(\})")
    REPLACE_WITH_SPACE = re.compile("(<br\s/><br\s/?)|(-)|(/)|(:).")
    tempArr = []
    for line in text_list:
        # send to tweet_processor
        tmpL = p.clean(line)
        # remove puctuation
        tmpL = REPLACE_NO_SPACE.sub("", tmpL.lower()) # convert all tweets to lower cases
        tmpL = REPLACE_WITH_SPACE.sub(" ", tmpL)
        tempArr.append(tmpL)
    return tempArr


def crp_algorithm(corpus, compute='cpu', cleaning=False):
    # cleaning
    if cleaning==True:
        corpus = clean_text(corpus)
        
    # Use of Related madule and function of sentence embedding 
    embedder = load_model(compute)
    corpus_embeddings = embedder.encode(corpus)
    print("shape of embedding vector :: ",corpus_embeddings.shape)
    
    # Start Of clustering CRP
    clusterVec = []  # tracks sum of vectors in a cluster

    vecs = corpus_embeddings.tolist()
    clusterIdx = [[]]  # array of index arrays. e.g. [[1, 3, 5], [2, 4, 6]]
    ncluster = 0
    # probablity to create a new table if new customer
    #If It's not strongly "similar" to any existing table
    pnew = 1.0 / (1 + ncluster)
    N = len(vecs)
    
    #rands = [random.random() for x in range(N)]  # N rand variables sampled from U(0, 1)
    ###################################

    df_cluster = pd.DataFrame()
    ###################################
    #cols=['new label']
    lst=[]
    for i in range(N):
        maxSim = -1
        maxIdx = 0
        v = vecs[i]
        #j = 0
        for j in range(ncluster):
            sim =  cosinesim(v,vecs[j])
            if sim > maxSim:
                maxIdx = j
                maxSim = sim
                # probablity to create a new table if new customer
                # is not strongly "similar" to any existing table
                if maxSim < pnew and j==ncluster-1 :
                    #if (rands[i] < pnew and j==ncluster-1):
                        clusterVec.append(v)
                        clusterIdx.append([i])
                        #df_cluster['label'] = df_cluster.append({'label': i}, ignore_index=True)
                        lst.append(maxIdx+1)
                        #df1 = pd.DataFrame(lst, columns=cols)
    
                        ncluster += 1
                        pnew = 1.0 / (1 + ncluster)
                        aaa = 1.0 / (1 + 1)
                        continue
            if (j==ncluster-1):
                 clusterIdx[maxIdx] = clusterIdx[maxIdx] + [i]
                 #df_cluster['label'] = df_cluster.append({'label': i}, ignore_index=True)
                 lst.append(maxIdx)
                 #df1 = pd.DataFrame(lst, columns=cols)
    
        if (i==0):
            #clusterIdx[maxIdx] = clusterIdx[maxIdx] + [i]
            clusterVec.append(v)
            clusterIdx[maxIdx] = clusterIdx[maxIdx] + [i]
            lst.append(ncluster)
            #df1 = pd.DataFrame(lst, columns=cols)
    
        if (ncluster == 0):
            ncluster += 1

    return lst

#%%




















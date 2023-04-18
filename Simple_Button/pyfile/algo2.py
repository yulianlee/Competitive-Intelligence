# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:24:38 2019

@author: common
"""

import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
from sklearn.linear_model import LogisticRegression  # Used Logistic Regression for prediction
import nltk
import pickle
import random
from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn as nn

punctuations = [",",".","(",")","-",".",'/'] #list of punctuations, expand if neccessary
new_model,logreg,sortedCompany = pickle.load(open("Simple_Button/pyfile/training_parameters.pkl","rb"))
title_list = pickle.load(open("Simple_Button/pyfile/title list","rb"))
bert_model = AutoModel.from_pretrained('./model')

def prediction(title):
    """
    Logistic Regression Model for predicing likely competitors.
    """
    new_proj = title.lower()

    for punctuation in punctuations: #O(n)
            new_proj = " ".join(new_proj.split(punctuation))

    test_tagged = TaggedDocument(words=tokenize_text(new_proj), tags=['test'])
    
    X_test = (test_tagged.tags[0], new_model.infer_vector(test_tagged.words, epochs= 10000))


    # Predicted probability for each company to be involved in the new project
    y_prob = logreg.predict_proba([X_test[1]])[0]
    # print(y_prob)
    # Maximum probability (i.e the probability for most likely company)

    # Preparing the visualsation dataframe
    visData = pd.DataFrame({'Company':sortedCompany['Company'],'Probability':y_prob,"FG":sortedCompany['FG']})

    # We only plot company with more than 1 % chance of competing, since average about 3.9 per project. (would deem 1% to be reasonable) 
    plottingSet = visData.loc[visData['Probability'] >= 0.01]
    
    top5 = plottingSet.sort_values(by=['Probability'],ascending = False).astype(str)

    top5likely = list(top5['Company'].values)

    return(list(zip(top5likely,top5['FG'].values)))


def get_value(sentence, description):

    tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
    # Tokenize the sentences
    tokenized_inputs = tokenizer(sentence, description, return_tensors='pt')

    with torch.no_grad():
        outputs = bert_model(**tokenized_inputs)
    
    output_values = outputs.numpy()

    upper, pred, lower = output_values[:, 0], output_values[:, 1], output_values[:, 2]

    return upper, pred, lower
    

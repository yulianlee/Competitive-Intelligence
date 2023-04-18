# -*- coding: utf-8 -*-
"""
Created on Fri May 24 15:24:38 2019

@author: common
"""

import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
from sklearn.linear_model import LogisticRegression  # Used Logistic Regression for prediction
from gensim.models.doc2vec import TaggedDocument
import nltk
import pickle
import random
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error

punctuations = [",",".","(",")","-",".",'/'] #list of punctuations, expand if neccessary
new_model,logreg,sortedCompany = pickle.load(open("Simple_Button/pyfile/training_parameters.pkl","rb"))

lda_model_10, id2word, d_topic_10, converted_currency = pickle.load(open("Simple_Button/pyfile/stuff to run","rb"))
title_list = pickle.load(open("Simple_Button/pyfile/title list","rb"))
stop_words = set(stopwords.words('english'))
nlp = pickle.load(open("Simple_Button/pyfile/spacy.pkl","rb"))

def tokenize_text(text):
        #token a string into individual words
        tokens = []
        for sent in nltk.sent_tokenize(text):
            for word in nltk.word_tokenize(sent):
                if len(word) < 2:
                    continue
                tokens.append(word.lower())
        return tokens



def prediction(title):
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

def get_value(sentence):

    predictions_for_amts_neo = clf_linear_reg.predict(x_test)

    test = np.array(get_topic(sentence))
    test = test.reshape(1,-1)
    return(round(max(float(clf_linear_reg.predict(test)),0),2),round(mean_absolute_error(y_test, predictions_for_amts_neo),2))

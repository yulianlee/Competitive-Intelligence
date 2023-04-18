# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:56:10 2019

@author: common
"""

import gensim
import spacy
from gensim.utils import simple_preprocess
from gensim.test.utils import common_texts
from gensim.corpora.dictionary import Dictionary
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error
import numpy as np
import pickle
import spacy


lda_model_10, id2word, d_topic_10, converted_currency = pickle.load(open("Simple_Button/pyfile/stuff to run","rb"))
title_list = pickle.load(open("Simple_Button/pyfile/title list","rb"))
stop_words = set(stopwords.words('english'))
nlp = pickle.load(open("Simple_Button/pyfile/spacy.pkl","rb"))

def sent_to_words(sentences):
    for sentence in sentences:
        yield(simple_preprocess(str(sentence), deacc=True))
        
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]



def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


def get_topic(sentence):
    new_corpus = [sentence]


    data_words = list(sent_to_words(new_corpus))


    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    
    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]
    
    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]

    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams,
                                    allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])


    other_corpus = [id2word.doc2bow(text) for text in data_lemmatized]


    unseen_doc = other_corpus[0]

    vector = lda_model_10[unseen_doc]  # get topic probability distribution for a document

    probs = vector[0]
    
    Topic_2 = probs[1][1] + probs[2][1] +probs[3][1] + probs[6][1]
    
    Topic_1 = probs[0][1]
    
    Topic_3 = probs[4][1] + probs[5][1] +probs[8][1] +probs[9][1]
    
    return (Topic_1, Topic_2, Topic_3)

def get_topic_dist(sentence):


    new_corpus = [sentence]


    data_words = list(sent_to_words(new_corpus))


    # Remove Stop Words
    data_words_nostops = remove_stopwords(data_words)

    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
    trigram = gensim.models.Phrases(bigram[data_words], threshold=100)
    
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)
    
    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]
    
    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]
    
    # Form Bigrams
    data_words_bigrams = make_bigrams(data_words_nostops)


    # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
    # python3 -m spacy download en

    # Do lemmatization keeping only noun, adj, vb, adv
    data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

    #print(data_lemmatized)


    other_corpus = [id2word.doc2bow(text) for text in data_lemmatized]


    unseen_doc = other_corpus[0]

    vector = lda_model_10[unseen_doc]  # get topic probability distribution for a document

    probs = vector[0]
    
    Topic_2 = probs[1][1] + probs[2][1] +probs[3][1] + probs[6][1]
    
    Topic_1 = probs[0][1]
    
    Topic_3 = probs[4][1] + probs[5][1] +probs[8][1] +probs[9][1]
    
    return (Topic_1, Topic_2, Topic_3)

def get_value(sentence):


    x_train, x_test, y_train, y_test = train_test_split(d_topic_10, 
                                                        converted_currency, 
                                                        test_size=0.2, random_state = 1)

    clf_linear_reg = LinearRegression()

    clf_linear_reg.fit(x_train, y_train)

    predictions_for_amts_neo = clf_linear_reg.predict(x_test)
    all_predictions_for_amts_neo = clf_linear_reg.predict(d_topic_10)


#    print("Mean Sqauare Error:", mean_squared_error(y_test, predictions_for_amts_neo))

#    coefficient_values_neo = list(all_predictions_for_amts_neo)

#    print("Mean Absolute Error:" , mean_absolute_error(y_test, predictions_for_amts_neo))

#    print(clf_linear_reg.coef_)
#    print(clf_linear_reg.intercept_)

    test = np.array(get_topic(sentence))
    test = test.reshape(1,-1)
    return(round(max(float(clf_linear_reg.predict(test)),0),2),round(mean_absolute_error(y_test, predictions_for_amts_neo),2))

def get_similar_sentence(sentence):
    new_sentence = sentence.split()
    opn = open("Simple_Button/pyfile/search", 'rb')
    model = pickle.load(opn )

    similar_doc = model.docvecs.most_similar(positive=[model.infer_vector(new_sentence, alpha = 0.01, epochs= 10000)],topn=3)
    #print(similar_doc)
    
    index_1 = int(similar_doc[0][0])
    index_2 = int(similar_doc[1][0])
    index_3 = int(similar_doc[2][0])
    prob_1 = similar_doc[0][1]
    prob_2 = similar_doc[1][1]
    prob_3 = similar_doc[2][1]
    
    similar_doc_1 = title_list[index_1]
    similar_doc_2 = title_list[index_2]
    similar_doc_3 = title_list[index_3]

    return (str(similar_doc_1),str(similar_doc_2),str(similar_doc_3))

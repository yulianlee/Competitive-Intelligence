# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# import mplcursors
import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import pymongo
import re
import pickle
# import matplotlib.pyplot as plt  # for visualisation
# from matplotlib.widgets import Button
# from matplotlib.text import Annotation
import json
import collections
#
# myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
# mydb = myclient["gebizz"]  #DB name
# mycol = mydb["GeBizCollection"]  #Collection name
#
# #Select only IT Service 408 entries out of 11k
# myquery = {}  #Query  -- can change
# #print(myquery)
# #ProcurementCategory
# mydoc = mycol.find()
# data = []
# for x in mydoc:
#     data.append(x)
data = pickle.load(open("Simple_Button/pyfile/all_stuff","rb"))
for entry in data:
    if len(entry['Awards']) == 1:
        for i in range(len(entry['Respondents'])):
            entry[('Respondent'+str(i))] = entry['Respondents'][str(i)]['CompanyName']
            entry[('_Respondent'+str(i)+"Value")] = entry['Respondents'][str(i)]['TotalPrice']
            #print(entry['Awards'])
        entry['AwardedTo'] = entry['Awards'][str(0)]['AwardedTo']
        entry['AwardedValue'] = entry['Awards'][str(0)]['AwardedValue']
    elif len(entry['Awards']) > 1:
        #entry['AwardedTo'] = 'Multi'
        pass
    else: # remove / just print anything for multiple award
        pass

def lowerCase(x):
    if isinstance(x, str):
        x.strip()
        return x.lower()
    return x

dataPreProcessed = pd.DataFrame(data)
del dataPreProcessed['Awards']
del dataPreProcessed['Respondents']

dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['Title'])] # remove any empty rows, if any
dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['AwardedValue'])]
dataPreProcessed = dataPreProcessed.applymap(lowerCase) # change all to lower case, preventing case sensitive

df = dataPreProcessed.reset_index()



def projs_per_agency():
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    return projs



def num_of_past_projs(agency):
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    #print(projs)
    return projs[agency]



def num_projs_graph(agency):
    z = {}
    colors = []
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    for num in range(1,25):
        colors.append('lightgrey')
        z[num] = 0
        for a in list(projs):
            num_projs = projs[a]
            if num_projs == num:
                z[num] += 1
    colors[projs[agency]-1]='lightcoral'
    plt.bar(range(len(z)), z.values(), align='center', color = colors)
    plt.xticks(range(len(z)), list(z.keys()))

    plt.xlabel('Number of Projects')
    plt.ylabel('Number of Agencies')
    plt.title('No. of Agencies that listed corresponding No. of Projects')

    plt.show()

    return None



def ags_projs(agency=None):
    de = df[df['Agency']==agency]
    ags_total = {}
    ags_projs = {}

    lowestbidslist = []
    awardedlowestbids = []

    for i in de.index.values: #for each project
        try:
            awardedamt = float(de.loc[i,'AwardedValue'][:-6])

            minbidamt = float(de.loc[i,'_Respondent0Value'][:-6])
            for n in range(1,17):
                if len(str(de.loc[i,'_Respondent{}Value'.format(n)])) > 3:
                    amt = float(de.loc[i,'_Respondent{}Value'.format(n)][:-6])
                    if amt < minbidamt:
                        minbidamt = amt

            lowestbidslist.append(minbidamt)
            if minbidamt == awardedamt:
                awardedlowestbids.append(minbidamt)

            if awardedamt<minbidamt:
                minbidamt = awardedamt

            maxbidamt = float(de.loc[i,'_Respondent0Value'][:-6])
            for m in range(1,17):
                if len(str(de.loc[i,'_Respondent{}Value'.format(m)])) > 3:
                    amt = float(de.loc[i,'_Respondent{}Value'.format(m)][:-6])
                    if amt > maxbidamt:
                        maxbidamt = amt

            if awardedamt>maxbidamt:
                maxbidamt = awardedamt

            if maxbidamt-minbidamt == 0:
                value = 0.5
            else:
                value = (awardedamt-minbidamt)/(maxbidamt-minbidamt)

        #values = list(value)

            projtitle = df.loc[i,'Title']

        except:
            None

#print(df.iloc[67,6:20][:-6])

    #print(agency)
    #print(projtitle)
    #print(ags_projs)
        if projtitle in ags_projs:
            ags_projs[projtitle] += value
        else:
            ags_projs[projtitle] = value

    return ags_projs



def ags_avg(agency):
    return np.mean(list(ags_projs(agency).values()))


def awardminbidgraph(agency):
    a = {}
    ap = ags_projs(agency)
    minbidsawarded = 0
    for x in ap:
        if ap[x] == 0:
            minbidsawarded += 1
    minbidawardprob = minbidsawarded/len(ap)
    return minbidawardprob



def convertToSGD(string):
    if isinstance(string, str):
        #print(string)
        x = string.split("(")
        amount = float(x[0])
        currency = x[1].strip()
        currency = currency[:-1]
        #print(amount)
        #print(currency)

        exchangeRate = {'sgd':1,'usd':1.36032,'eur':1.52292,
                        'myr':0.32874,'chf':1.33804,'gbp':1.76,
                        "aud":0.95,"cnh":0.2,"jpy":0.013,"qar":0.38,
                        "bnd":1,"aed":0.37,"nzd":0.9,"idr":0.000095,
                        "sek":0.14,"cad":1.02,"php":0.026,"inr":0.02}

        try:
            sgdValue = amount * exchangeRate[currency]
            return sgdValue
        except:
            try:
                currency = currency.split(")")[0]
                sgdValue = amount * exchangeRate[currency]
                return sgdValue
            except:
                print(currency)

def total_avg(agency):



    subset = df[df['Agency']==agency]

    subset['AwardedValue'] = subset['AwardedValue'].apply(convertToSGD)
    total = round(np.sum(subset['AwardedValue']),2)
    avg = round(np.mean(subset['AwardedValue']),2)

    test = pd.DataFrame.from_dict(ags_projs(agency).items())
    test.rename({0:'Title',1:'tendancy'},axis=1,inplace=True)
    result = pd.merge(test, subset[['Title','AwardedTo','AwardedValue']], on=['Title']).to_json(orient='records')

    return total,avg,result

def procurement_category(agency):

    subset = df[df['Agency']==agency]
    procurement_cat = list(subset["ProcurementCategory"])

    return(procurement_cat)

# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 15:22:49 2019

@author: Jia Yi
"""

import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
import pymongo
import matplotlib.pyplot as plt  # for visualisation

# myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
# mydb = myclient["gebizz"]  #DB name
# mycol = mydb["GeBizCollection"]  #Collection name
#
# #Select only IT Service 408 entries out of 11k
# myquery = {'ProcurementCategory': 'IT&Telecommunication ⇒ IT Services & Software Development '}  #Query  -- can change
#
# #ProcurementCategory
# mydoc = mycol.find(myquery)
# data = []
# for x in mydoc:
#     data.append(x)
data = pickle.load(open("Simple_Button/pyfile/all_stuff","rb"))
for entry in data:
    if len(entry['Awards']) == 1:
        for i in range(len(entry['Respondents'])):
            entry[('Respondent'+str(i))] = entry['Respondents'][str(i)]['CompanyName']
            entry[('_Respondent'+str(i)+"Value")] = entry['Respondents'][str(i)]['TotalPrice']
        entry['AwardedTo'] = entry['Awards'][str(0)]['AwardedTo']
        entry['AwardedValue'] = entry['Awards'][str(0)]['AwardedValue']
        pass

def lowerCase(x):
    if isinstance(x, str):
        x = x.strip()
        return x.lower()
    return x

dataPreProcessed = pd.DataFrame(data)

del  dataPreProcessed['Awards']
del  dataPreProcessed['Respondents']

dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['Title'])] # remove any empty rows, if any
dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['AwardedValue'])]
dataPreProcessed = dataPreProcessed.applymap(lowerCase) # change all to lower case, preventing case sensitive

def convertToSGD(string):
    if isinstance(string, str):
        x = string.split("(")
        amount = float(x[0])
        currency = x[1].strip()
        currency = currency[:-1]

        exchangeRate = {'sgd':1,'usd':1.36032,'eur':1.52292,'myr':0.32874,'chf':1.33804,'gbp':1.76}

        sgdValue = amount * exchangeRate[currency]
        return sgdValue

maxRespondent = len(list(dataPreProcessed.filter(regex="^Resp")))

for i in range(maxRespondent):
    dataPreProcessed['_Respondent'+str(i)+'Value'] = dataPreProcessed['_Respondent'+str(i)+'Value'].apply(convertToSGD)
dataPreProcessed['AwardedValue'] = dataPreProcessed['AwardedValue'].apply(convertToSGD)

dataPreProcessed['MeanBid'] = dataPreProcessed.filter(regex="^_Resp").mean(axis=1)

for i in range(maxRespondent):
    dataPreProcessed['Differences'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['AwardedValue']
    dataPreProcessed['_DifferencesFromMean'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['MeanBid']
dataPreProcessed = dataPreProcessed.sort_values(by=['AwardedValue'],ascending=True)



company1 = input("First Company: ")
company2 = input("Second Company: ")




#number of projects = competitorlist[company1]
def no_of_bids(company):
    competitorlist = {}
    for i in range(0,408):
        for j in range(0,17):
            try:
                name = dataPreProcessed["Respondent"+str(j)][i]
                if name not in competitorlist:
                    competitorlist[name]=1
                else:
                    competitorlist[name]+=1
            except:
                pass
    return competitorlist[company]




#projectdic = {project:{competitor:bidamt}}
titles = []
for i in range(0,408):
    try:
        if np.isnan(dataPreProcessed['AwardedValue'][i])==False:
            titles.append(dataPreProcessed['Title'][i])
    except:
        pass

projectdic = dict.fromkeys(titles, 0)

for i in range(0,408):
    try:
        a = {}
        for j in range(0,17):
            try:
                if np.isnan(dataPreProcessed["Respondent"+str(j)][i])==True:
                    pass
            except:
                a[dataPreProcessed["Respondent"+str(j)][i]]=dataPreProcessed['_Respondent'+str(j)+'Value'][i]
        projectdic[dataPreProcessed['Title'][i]]=a
    except:
        pass



#minmax & biddiff
minmax = {}
mmdiff = {}
for pj in projectdic:
    minbid = 1000000000
    maxbid = 0
    for bid in projectdic[pj]:
        if projectdic[pj][bid]<minbid:
            minbid = projectdic[pj][bid]
        if projectdic[pj][bid]>maxbid:
            maxbid = projectdic[pj][bid]
    minmax[pj] = [minbid,maxbid]
    mmdiff[pj] = maxbid-minbid


competitors = {}
#competitors = {company:{project:diff}}
bidcount = {}
#bidcount = {company:no. of bids}
wincount = {}
#wincount = {company:no. of wins}
competitorpjs = {}
#competitorpjs = {company:[projects]}
totalbids = {}
#totalbids = {company: total bidded amount for all projects}
index = {}
#index = {company:{project:bid index}}
companiesdic = {}
#companiesdic = {company:{project:[date,title,bidamt,awardval,diff,indexval]}}

for i in range(0,408):
    for j in range(0,17):
        try:
            name = dataPreProcessed["Respondent"+str(j)][i]
            project = dataPreProcessed['Title'][i]
            bid = dataPreProcessed['_Respondent'+str(j)+'Value'][i]
            diff = bid - dataPreProcessed['AwardedValue'][i]

            if name not in competitors:
                competitors[name]={project:diff}
            else:
                competitors[name][project]=diff
            if name not in bidcount:
                bidcount[name]=1
            else:
                bidcount[name]+=1
            if name not in wincount:
                if diff == 0:
                    wincount[name]=1
                else:
                    wincount[name]=0
            else:
                if diff == 0:
                    wincount[name]+=1
            if name not in competitorpjs:
                competitorpjs[name]=[project]
            else:
                competitorpjs[name].append(project)
            if name not in totalbids:
                totalbids[name]=bid
            else:
                totalbids[name]+=bid

            if mmdiff[project]>0:
                bidindex=(bid-(float(minmax[project][0])))/(mmdiff[project])
            else:
                bidindex=0.5
            if name not in index:
                index[name]={project:bidindex}
            else:
                index[name][project]=bidindex

            if name not in companiesdic:
                companiesdic[name]={project:[dataPreProcessed['TenderClosingDate'][i],project,bid,dataPreProcessed['AwardedValue'][i],diff,bidindex]}
            else:
                companiesdic[name][project]=[dataPreProcessed['TenderClosingDate'][i],project,bid,dataPreProcessed['AwardedValue'][i],diff,bidindex]


        except:
            pass


def date(company,project):
    return companiesdic[company][project][0]

def title(company,project):
    return companiesdic[company][project][1]

def bidamt(company,project):
    return companiesdic[company][project][2]

def awardval(company,project):
    return companiesdic[company][project][3]

def diff(company,project):
    return companiesdic[company][project][4]

def indexval(company,project):
    return companiesdic[company][project][5]




def avgbidindex(company):
    totalindex = 0
    for proj in index[company]:
        totalindex += index[company][proj]
    avgindex = totalindex/no_of_bids(company)
    return avgindex




#BID INDEX PLOT (company)
def indexplot(company):
    plt.title(company)
    plt.xticks(range(len(index[company])), list(index[company].keys()))
    plt.ylabel("Bid Index (Per Project)")
    plt.ylim(-0.1,1.1)
    plt.xticks([])
    plt.plot(range(len(index[company])), index[company].values(), 'ro', color='black')#,label="{}:".format(list(ags_avg)[i]))

    x = list(index[company].keys())
    y = list(index[company].values())
    label = [''*len(index[company].keys())]

    plt.show()
    return None




def totalbidamt(company):
    return totalbids[company]

def avgbidval(company):
    avgbidval = totalbidamt(company)/no_of_bids(company)
    return avgbidval



def winrate(company):
    winrate = {k: wincount[k] / float(bidcount[k]) for k in bidcount if k in wincount}
    return winrate[company]



#WIN RATE GRAPH
def winrategraph(company1,company2):

    winrate = {k: wincount[k] / float(bidcount[k]) for k in bidcount if k in wincount}

    fig, ax = plt.subplots()
    data = winrate.values()

    N, bins, patches = ax.hist(data, bins=[0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1], edgecolor='white', linewidth=1)

    n = int(winrate[company1]*10)

    if n<10:
        for i in range(0,n):
            patches[i].set_facecolor('gainsboro')
        for i in range(n,n+1):
            patches[i].set_facecolor('dodgerblue')
        for i in range(n+1,10):
            patches[i].set_facecolor('gainsboro')
    else:
        for i in range(0,n-1):
            patches[i].set_facecolor('gainsboro')
        for i in range(n-1,n):
            patches[i].set_facecolor('dodgerblue')

        m = int(winrate[company2]*10)

    if m<10:
        for i in range(m,m+1):
            patches[i].set_facecolor('tomato')
    else:
        for i in range(m-1,m):
            patches[i].set_facecolor('tomato')

    plt.title('Company Winning Rate')
    plt.xlabel('Win Rate')
    plt.ylabel('Number of Companies')
    plt.bar([0],[0], label=company1, color='dodgerblue')
    plt.bar([0],[0], label=company2, color='tomato')
    plt.xlim(-0.02,1.02)
    plt.legend()
    plt.show()
    return None


#BID DIFFERENCE PLOT (company)
def biddiffplot(company):
    plt.title(company)
    plt.xticks(range(len(competitors[company])), list(competitors[company].keys()))
    plt.ylabel("Difference From Award Value")
    plt.xticks([])
    plt.axhline(y=0)
    plt.plot(range(len(competitors[company])), competitors[company].values(), 'ro', color='black')#,label="{}:".format(list(ags_avg)[i]))
    limit=[]
    for value in list(competitors[company].values()):
        val = abs(value)
        limit.append(val)
    plt.ylim(-(max(limit)+max(limit)/10),(max(limit)+max(limit)/10))

    x = list(competitors[company].keys())
    y = list(competitors[company].values())
    label = [''*len(competitors[company].keys())]
    plt.show()
    return None

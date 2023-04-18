# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:29:23 2019

@author: common
"""
import pickle
import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
# from tqdm import tqdm
# tqdm.pandas(desc="progress-bar")
# import seaborn as sns
# import matplotlib.pyplot as plt  # for visualisation
# import pymongo # for database access
# import matplotlib as mpl
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure

# plt.style.use('ggplot')

# myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
# mydb = myclient["gebizz"]  #DB name
# mycol = mydb["GeBizCollection"]  #Collection name
#
# #Select only IT Service 408 entries out of 11k
# myquery = {}  #Query
# #print(myquery)
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
            #print(entry['Awards'])
        entry['AwardedTo'] = entry['Awards'][str(0)]['AwardedTo']
        entry['AwardedValue'] = entry['Awards'][str(0)]['AwardedValue']
    elif len(entry['Awards']) > 1:
        #entry['AwardedTo'] = 'Multi'
#        print("\n" + entry['Title'] + "  !MULTI")
#        print(entry['Agency'])
#        print(entry['Awards'])
        pass
        #data.remove(entry)
    else: # remove / just print anything for multiple award
#        print("\n" + entry['Title'] + "  !NONE")
#        print(entry['Agency'])
#        print(entry['Awards'])
        pass
        #data.remove(entry)

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

# print(dataPreProcessed.shape)
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
                pass
                #print(currency)

maxRespondent = len(list(dataPreProcessed.filter(regex="^Resp")))
for i in range(maxRespondent):
    dataPreProcessed['_Respondent'+str(i)+'Value'] = dataPreProcessed['_Respondent'+str(i)+'Value'].apply(convertToSGD)
    #df['DifferenceRespondent'+str(i)] = df['_Respondent'+str(i)+'Value']
dataPreProcessed['AwardedValue'] = dataPreProcessed['AwardedValue'].apply(convertToSGD)

dataPreProcessed['MeanBid'] = dataPreProcessed.filter(regex="^_Resp").mean(axis=1)
#print(maxRespondent)
for i in range(maxRespondent):
    dataPreProcessed['Differences'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['AwardedValue']
    dataPreProcessed['_DifferencesFromMean'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['MeanBid']

df = dataPreProcessed.filter(regex="^Diff")
# print(df.shape)
# df = df.applymap(lambda x: x == float(0.0)) #remove none value-based awards
#df.any(axis='columns')
# dataPreProcessed[df.any(axis='columns')]  #remove case where only 1 bidder
dfMoreThanOne = dataPreProcessed.filter(regex="^Diff")

pData = dfMoreThanOne.join(dataPreProcessed.filter(regex="^Respon"))

# print(pData.shape)
companyData = pData.filter(regex="^Respon").melt()

pData = (dfMoreThanOne.melt()).join(companyData,lsuffix="_diff",rsuffix="_comp")
pData['AwardedValue'] = list(dfMoreThanOne.join(dataPreProcessed['AwardedValue'])["AwardedValue"].values)*maxRespondent
pData['Title'] =list(dfMoreThanOne.join(dataPreProcessed['Title'])['Title'].values)*maxRespondent
pData['Agency'] = list(dfMoreThanOne.join(dataPreProcessed['Agency'])['Agency'].values)*maxRespondent

pData = pData[['value_comp','value_diff','AwardedValue','Title','Agency']].sort_values(by=['value_comp']) #5406 rows
# pData = pData.dropna() #648 rows
pData[pData == 0.0] = np.nan


pData.rename(columns={'value_diff':'Times_won',
                          'AwardedValue':'Times_bid',
                     'value_comp':'Company_name'},
                 inplace=True)


#print(best5)
#print(gdf.sort_values(by=['Winning Rate'],ascending=False).tail(5))
result = dfMoreThanOne.join(dataPreProcessed.filter(regex="^_Diff")).filter(regex="^_Diff")
#result
PlotData = (result.melt()).join(companyData,lsuffix="_diff",rsuffix="_comp")
PlotData['AwardedValue'] = list(dfMoreThanOne.join(dataPreProcessed['AwardedValue'])["AwardedValue"].values)*maxRespondent
PlotData['AwardedTo'] = list(dfMoreThanOne.join(dataPreProcessed['AwardedTo'])["AwardedTo"].values)*maxRespondent
PlotData['Title'] =list(dfMoreThanOne.join(dataPreProcessed['Title'])['Title'].values)*maxRespondent
PlotData['Agency'] =list(dfMoreThanOne.join(dataPreProcessed['Agency'])['Agency'].values)*maxRespondent
PlotData['MeanBid'] =list(dfMoreThanOne.join(dataPreProcessed['MeanBid'])['MeanBid'].values)*maxRespondent

# print(PlotData.shape)
PlotData = PlotData[['value_comp','value_diff','AwardedValue','Title','MeanBid','Agency','AwardedTo']].sort_values(by=['value_comp']) #5406 rows
# PlotData = PlotData.dropna() #648 rows
# print(PlotData.shape)
PlotData['Difference_From_Award'] = pData['Times_won']
PlotData['Won'] = PlotData['value_comp'] == PlotData['AwardedTo']
PlotData['Won'] = PlotData['Won'].astype('str')
PlotData.fillna(0,inplace=True)
PlotData.rename(columns={'value_diff':'Difference_From_Mean',
                     'value_comp':'Company_name'},
                 inplace=True)

# sns.set(style='ticks')



#fg = sns.FacetGrid(data=PlotData[PlotData['Company_name']=='ncs pte. ltd.'],
#                       hue='Won',aspect=1.61)
#plt.subplots_adjust(top=0.9)
#fg.fig.suptitle('ncs pte. ltd.')
#fg.map(plt.scatter, 'MeanBid',
#       'Difference_From_Mean').add_legend()

# plt.ion()
def plot_difference_from_mean(company,agency="not selected"):
    company = company.lower()
    agency = agency.lower()
    if agency == "not selected":
        subset = PlotData[PlotData['Company_name']==company].sort_values(by=["Won","AwardedValue"],ascending=False)
        return subset[['AwardedValue','Difference_From_Mean','Agency','Title','Won','AwardedTo']].to_json(orient='records')
    else:
        subset = PlotData[PlotData['Company_name']==company].sort_values(by=["Won","AwardedValue"],ascending=False)
        subsubset = subset[subset['Agency'] == agency]
        return subsubset[['AwardedValue','Difference_From_Mean','Agency','Title','Won','AwardedTo']].to_json(orient='records')


def bid_range(company,agency = "not selected"):
    company = company.lower()
    agency = agency.lower()
    if agency == "not selected":
        try:
            y = PlotData[PlotData['Company_name'] == company]['Difference_From_Mean'].values
            x = PlotData[PlotData['Company_name'] == company]['AwardedValue'].values
            z = PlotData[PlotData['Company_name'] == company]['Difference_From_Mean'].values  + \
            PlotData[PlotData['Company_name'] == company]['AwardedValue'].values

            #print(np.median(z))
            iqr = np.subtract(*np.percentile(z, [75, 25]))
            if np.median(z)-1.5*iqr < 0:
                return (0,round(np.median(z)+1.5*iqr,2))
            else:
                return (round(np.median(z)-1.5*iqr,2),round(np.median(z)+1.5*iqr,2))
        except:
            return (0,0)
    else:
        try:
            subset = PlotData[PlotData['Agency']==agency.lower()]
            y = subset[subset['Company_name'] == company]['Difference_From_Mean'].values
            x = subset[subset['Company_name'] == company]['AwardedValue'].values
            z = subset[subset['Company_name'] == company]['Difference_From_Mean'].values  + \
            subset[subset['Company_name'] == company]['AwardedValue'].values

            #print(np.median(z))
            iqr = np.subtract(*np.percentile(z, [75, 25]))
            if np.median(z)-1.5*iqr < 0:
                return (0,round(np.median(z)+1.5*iqr,2))
            else:
                return (round(np.median(z)-1.5*iqr,2),round(np.median(z)+1.5*iqr,2))
        except:
            return (0,0)

def win_rate(company,agency = "not selected"):
    company = company.lower()
    agency = agency.lower()
    if agency == "not selected":
        try:
            bids = PlotData[PlotData['Company_name']==company].count()[0]
            wons = sum(PlotData[PlotData['Company_name']==company]['Won'] == "True")
            try:
                rate = round(wons/float(bids),2)
        #        print(bids,wons,rate)
                return (int(bids),int(wons),float(rate))
            except:
                return (int(bids),int(wons),0)
        except:
            return (0,0,0)
    else:
        subset = PlotData[PlotData['Agency']==agency.lower()]
        bids = subset[subset['Company_name']==company].count()[0]
        wons = sum(subset[subset['Company_name']==company]['Won'] == "True")
        try:
            rate = round(wons/float(bids),2)
    #        print(bids,wons,rate)
            return (int(bids),int(wons),float(rate))
        except:
            return (int(bids),int(wons),0)

def total_sum(company,agency = "not selected"):
    company = company.lower()
    agency = agency.lower()
    if agency == "not selected":
        try:
            total = round(np.sum(PlotData[PlotData['Company_name'] == company]['Difference_From_Mean'].values  + \
            PlotData[PlotData['Company_name'] == company]['AwardedValue'].values),2)
            #print(total)
            subset = PlotData[PlotData['Company_name'] == company]
            #print(subset)
            won = np.sum(subset[subset['Won'] == 'True']['AwardedValue'])
            #print(won)
            return total,won
        except:
            return (0,0)
    else:
        try:
            subset = PlotData[PlotData['Agency']==agency.lower()]
            total = round(np.sum(subset[subset['Company_name'] == company]['Difference_From_Mean'].values  + \
            subset[subset['Company_name'] == company]['AwardedValue'].values),2)
            #print(total)
            subsubset = subset[subset['Company_name'] == company]
            #print(subset)
            won = np.sum(subsubset[subsubset['Won'] == 'True']['AwardedValue'])
            #print(won)
            return total,won
        except:
            return (0,0)

def company_list():
    return list(gdf['Company_name'].values)

#plot_difference_from_mean('ncs pte. ltd.')
d = pickle.load(open("Simple_Button/pyfile/companydictdataframes","rb"))
def get_FG(company):
    company = company.lower()
    award = 0
    for i in range(len(d[company])):
        value = d[company]["AwardedValue"].max()

    if value<= 100000:
        FG = "S2"
    elif 100000< value <= 250000:
        FG = "S3"
    elif 250000< value <= 500000:
        FG = "S4"
    elif 500000< value <= 1000000:
        FG = "S5"
    elif 1000000< value <= 3000000:
        FG = "S6"
    elif 3000000< value <= 5000000:
        FG = "S7"
    elif 5000000< value <= 10000000:
        FG = "S8"
    elif 10000000< value <= 30000000:
        FG = "S9"
    elif 30000000< value:
        FG = "S10"
    return (FG)

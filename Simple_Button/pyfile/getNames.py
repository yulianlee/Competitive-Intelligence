import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import pymongo
import re
import json

pd.set_option('mode.chained_assignment', None)

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

de = dataPreProcessed.filter(regex="^Resp").melt().dropna()
companyList = sorted(de['value'].str.strip().unique())
# print(companyList)
companies = []
for i in range(0,len(companyList)):
    companies += [{"id":i,"company":companyList[i]}]
# print(companies)
Agencies = []
a =  ["Not Selected"] + sorted(df['Agency'].str.strip().unique()[:-1])
AgencyList = [str(x).title() for x in a]
for i in range(0,len(AgencyList)):
    Agencies += [{"id":i,"Agency":AgencyList[i]}]

df1 = df[['Agency','AwardedTo','AwardedValue']]

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

df1['AwardedValue']=df1['AwardedValue'].apply(convertToSGD)


topAByNum = df1[['Agency','AwardedTo']].groupby(['Agency']).count().sort_values(['AwardedTo'],ascending=False).reset_index().head().to_dict('records')
topAByVal = df1[['Agency','AwardedValue']].groupby(['Agency']).sum().sort_values(['AwardedValue'],ascending=False).reset_index().head().round(2).to_dict('records')
topCbyNum = df1[['AwardedValue','AwardedTo']].groupby(['AwardedTo']).count().sort_values(['AwardedValue'],ascending=False).reset_index().head().to_dict('records')
topCbyVal = df1[['AwardedValue','AwardedTo']].groupby(['AwardedTo']).sum().sort_values(['AwardedValue'],ascending=False).reset_index().head().round(2).to_dict('records')

# overview = [{"companies":companies,"Agencies":Agencies,"topAByNum":topAByNum,"topAByVal":topAByVal,"topCbyNum":topCbyNum,"topCbyVal":topCbyVal}]

# print(overview)
print(json.dumps(companies))
print(json.dumps(Agencies))
print(json.dumps(topAByNum))
print(json.dumps(topAByVal))
print(json.dumps(topCbyNum))
print(json.dumps(topCbyVal))

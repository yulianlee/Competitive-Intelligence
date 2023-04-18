import sys
import json
import pymongo
import re
import random
import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import collections
import pickle
from collections import Counter

a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	category = param['OutputFromBrowser']

except:
	category = 1 #arbitrary


def top_3_by_value(category):
    d= pickle.load(open("Simple_Button/pyfile/dictionary_dataframe_2","rb"))
    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
        # else:
        #     return (json.dumps("ERROR"))
    awarded_vals = dataframe["AwardedValue"]
    index = [] #this returns the index for the top 3 projs in the dataframe
    for item in sorted( [(x,i) for (i,x) in enumerate(awarded_vals)], reverse=True )[:3]:
        index.append(item[1])
#     print( sorted( [(x,i) for (i,x) in enumerate(awarded_vals)], reverse=True )[:3])

    top1 = []
    top2 = []
    top3 = []
    value1 = dataframe.iloc[index[0]]["AwardedValue"]
    agency1 = dataframe.iloc[index[0]]["Agency"]
    awarded_to1 = dataframe.iloc[index[0]]["AwardedTo"]
    awarded_date1 = dataframe.iloc[index[0]]["AwardedDate"]
    proc_cat1 = dataframe.iloc[index[0]]["ProcurementCategory"]
    no_awarded1 = dataframe.iloc[index[0]]["NoOfSuppliersAwarded"]
    proc_type1 = dataframe.iloc[index[0]]["ProcurementType"]
    proc_method1 = dataframe.iloc[index[0]]["ProcurementMethod"]
    tender_id1 = dataframe.iloc[index[0]]["QuotationNo"].upper()
    title1 = dataframe.iloc[index[0]]["Title"].upper()

    top1.append(value1)
    top1.append(agency1)
    top1.append(awarded_to1)
    top1.append(awarded_date1)
    top1.append(proc_cat1)
    top1.append(proc_type1)
    top1.append(proc_method1)
    top1.append(tender_id1)
    top1.append(title1)

    value2 = dataframe.iloc[index[1]]["AwardedValue"]
    agency2 = dataframe.iloc[index[1]]["Agency"]
    awarded_to2 = dataframe.iloc[index[1]]["AwardedTo"]
    awarded_date2 = dataframe.iloc[index[1]]["AwardedDate"]
    proc_cat2 = dataframe.iloc[index[1]]["ProcurementCategory"]
    no_awarded2 = dataframe.iloc[index[1]]["NoOfSuppliersAwarded"]
    proc_type2 = dataframe.iloc[index[1]]["ProcurementType"]
    proc_method2 = dataframe.iloc[index[1]]["ProcurementMethod"]
    tender_id2 = dataframe.iloc[index[1]]["QuotationNo"].upper()
    title2 = dataframe.iloc[index[1]]["Title"].upper()

    top2.append(value2)
    top2.append(agency2)
    top2.append(awarded_to2)
    top2.append(awarded_date2)
    top2.append(proc_cat2)
    top2.append(proc_type2)
    top2.append(proc_method2)
    top2.append(tender_id2)
    top2.append(title2)

    value3 = dataframe.iloc[index[2]]["AwardedValue"]
    agency3 = dataframe.iloc[index[2]]["Agency"]
    awarded_to3 = dataframe.iloc[index[2]]["AwardedTo"]
    awarded_date3 = dataframe.iloc[index[2]]["AwardedDate"]
    proc_cat3 = dataframe.iloc[index[2]]["ProcurementCategory"]
    no_awarded3 = dataframe.iloc[index[2]]["NoOfSuppliersAwarded"]
    proc_type3 = dataframe.iloc[index[2]]["ProcurementType"]
    proc_method3 = dataframe.iloc[index[2]]["ProcurementMethod"]
    tender_id3 = dataframe.iloc[index[2]]["QuotationNo"].upper()
    title3 = dataframe.iloc[index[2]]["Title"].upper()

    top3.append(value3)
    top3.append(agency3)
    top3.append(awarded_to3)
    top3.append(awarded_date3)
    top3.append(proc_cat3)
    top3.append(proc_type3)
    top3.append(proc_method3)
    top3.append(tender_id3)
    top3.append(title3)
    dict1 = {"top1":top1 ,"top_2":top2,"top3":top3}

    #Top 5 Agency by Project

    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
    agencies = dataframe["Agency"]
    dic = {}
    for item in agencies:
        if item not in dic:
            dic[item]=0
        elif item in dic.keys():
            dic[item]+=1


    c = Counter(dic)
    mc2 = c.most_common(5)

    dict2 = {"mc2":mc2}


    # TOP 5 Agency by Spending
    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
    agencies = dataframe["Agency"]
    dic = {}
    for item in agencies:
        if item not in dic:
            dic[item.upper()]=0
        elif item in dic.keys():
            continue
    for i in range(len(dataframe["Agency"])):
        awarded_val = dataframe.iloc[i]['AwardedValue']
        agency = dataframe.iloc[i]["Agency"].upper()
        if agency in dic.keys():
            dic[agency]+=awarded_val

    c = Counter(dic)
    mc3 = c.most_common(5)

    dict3 = {"mc3":mc3}


    #Top 5 companies by project awarded
    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
    companies = dataframe["AwardedTo"]
    dic = {}
    for company in companies:
        if company.upper() not in dic.keys():
            dic[company.upper()]=0
        elif company.upper() in dic.keys():
            dic[company.upper()]+=1

    c = Counter(dic)
    mc4 = c.most_common(5)

    dict4 = {"mc4":mc4}

    # Top 5 companies by value
    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
    companies = dataframe["AwardedTo"]
    dic = {}
    for company in companies:
        if company.upper() not in dic.keys():
            dic[company.upper()]=0
        elif item in dic.keys():
            continue
    for i in range(len(dataframe["AwardedTo"])):
        awarded_val = dataframe.iloc[i]['AwardedValue']
        company = dataframe.iloc[i]["AwardedTo"].upper()
        if company in dic.keys():
            dic[company]+=awarded_val

    c = Counter(dic)
    mc5 = c.most_common(5)

    dict5 = {"mc5":mc5}


    all_dict = [dict1,dict2,dict3,dict4,dict5]

    # return (json.dumps(dict1,dict2,dict3,dict4))
    return (json.dumps(all_dict))

# Create address variable in the temp folder
address = 'Simple_Button/temp/'+"intro_page"+''+str(random.randint(1,10000001))+'.txt'

# Write a file to the address
with open(address, 'w') as outfile:
	json.dump(top_3_by_value(category), outfile)

# Output the address for retrieval using JS
print(address)

import sys
import json
import pymongo
import re
import random
import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import collections
import pickle

a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	query = param['OutputFromBrowser']

except:
	query = 1 #arbitrary


bulktenders= pickle.load(open("Simple_Button/pyfile/bulk_tenders","rb"))
id_list = pickle.load(open("Simple_Button/pyfile/id_list","rb"))

def bulk_detail(query):
    for i in range(len(id_list)):
        if query == id_list[i]:
            index = i
        else:
            continue

    entry = bulktenders.iloc[index]
    agency = entry["Agency"]
    date = entry['AwardedDate']
    no_awarded = entry['NoOfSuppliersAwarded']
    method = entry['ProcurementMethod']
    ptype = entry['ProcurementType']
    pdate = entry['PublishedDate']
    qno = entry['QuotationNo']
    qtype = entry['QuotationType']
    cdate = entry['TenderClosingDate']
    title = entry['Title']
    _id = entry['_id']
    awards = entry["Awards"]
    procurementcategory = entry["ProcurementCategory"]


    winners = []
    winning_amts = []

    for i in awards.keys():
        winner = awards[i]["AwardedTo"]
        winning_amt = awards[i]["AwardedValue"]
        winners.append(winner)
        winning_amts.append(winning_amt)

    dict1 = {"agency":agency ,"date":date,"no_awarded":no_awarded,"method":method, "ptype":ptype, "pdate":pdate, "qno":qno, "qtype":qtype, "cdate":cdate, "title":title, "_id":_id, "awards":awards, "pcat":procurementcategory}

    return (json.dumps(dict1))
# Create address variable in the temp folder
address = 'Simple_Button/temp/'+"bulksearch"+''+str(random.randint(1,10000001))+'.txt'

# Write a file to the address
with open(address, 'w') as outfile:
	json.dump(bulk_detail(query), outfile)

# Output the address for retrieval using JS
print(address)

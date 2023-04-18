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
import pygal
from pygal.style import Style
import datetime
a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))
year = param['year']

try:
	agency= param['OutputFromBrowser']

except:
	agency = 1 #arbitrary

agency = agency.lower()
# d = pickle.load(open("./pyfile/agency_dataframe","rb"))
d = pickle.load(open("Simple_Button/pyfile/allagency","rb"))

def to_datetime(d):
 day, month, year = map(int, d.split(' '))
 return datetime.datetime(year, month, day, 0, 0, 0)

def get_proc_cat(agency, year):
    df = d[agency]
    dates = list(df["Dates"])
    values = list(df["AwardedValue"])
    p_cats = list(df["ProcurementCategory"])

    a = '01 01 2013'
    b = '31 12 2013'
    _a = to_datetime(a)
    _b = to_datetime(b)

    values_per_year = {'all':{},2013:{}, 2014:{}, 2015:{},2016:{},2017:{},2018:{}}
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2013]:
                values_per_year[2013][p_cat] = []
                values_per_year[2013][p_cat].append(value)
            else:
                values_per_year[2013][p_cat].append(value)

    a = '01 01 2014'
    b = '31 12 2014'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2014]:
                values_per_year[2014][p_cat] = []
                values_per_year[2014][p_cat].append(value)
            else:
                values_per_year[2014][p_cat].append(value)
    a = '01 01 2015'
    b = '31 12 2015'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2015]:
                values_per_year[2015][p_cat] = []
                values_per_year[2015][p_cat].append(value)
            else:
                values_per_year[2015][p_cat].append(value)
    a = '01 01 2016'
    b = '31 12 2016'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2016]:
                values_per_year[2016][p_cat] = []
                values_per_year[2016][p_cat].append(value)
            else:
                values_per_year[2016][p_cat].append(value)
    a = '01 01 2017'
    b = '31 12 2017'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2017]:
                values_per_year[2017][p_cat] = []
                values_per_year[2017][p_cat].append(value)
            else:
                values_per_year[2017][p_cat].append(value)
    a = '01 01 2018'
    b = '31 12 2018'
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year[2018]:
                values_per_year[2018][p_cat] = []
                values_per_year[2018][p_cat].append(value)
            else:
                values_per_year[2018][p_cat].append(value)
    a = '01 01 2013'
    b = '31 12 2018'
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            if p_cat not in values_per_year['all']:
                values_per_year['all'][p_cat]=[]
                values_per_year['all'][p_cat].append(value)
            else:
                values_per_year['all'][p_cat].append(value)




    dict = {"cats":list(values_per_year['all'].keys())}
    return json.dumps(dict)


# Create address variable in the temp folder
address = 'Simple_Button/temp/'+str(agency)+"categories"+'.txt'


with open(address, 'w') as outfile:
    json.dump(get_proc_cat(agency,year), outfile)

print(address)

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

try:
	company= param['OutputFromBrowser']

except:
	company = 1 #arbitrary

company = company.lower()
d = pickle.load(open("Simple_Button/pyfile/companydictdataframes","rb"))
def cleaning(item):
#     if isinstance(x, str):
    item = item.replace('⇒','')
    item = item.replace('‡','')
    item = item.replace('â','')
    item = item.replace('?','')
    item = item.replace("’",'')
    item = item.replace('’','')
    item = item.replace(" ", "-")

    return item

def to_datetime(d):
    day, month, year = map(int, d.split(' '))
    return datetime.datetime(year, month, day, 0, 0, 0)

def date_retrieval_all(company, year):
    df = d[company]
    dates = list(df["Dates"])
    values = list(df["AwardedValue"])
    p_cats = list(df["ProcurementCategory"])
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    indexes={}
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:

            indexes[i] = [date,value, p_cat]
    total = {}
    for i in indexes.keys():
        value = indexes[i][1]
        p_cat = indexes[i][2]

        if p_cat not in total.keys():
            total[p_cat] = value
        elif p_cat in total.keys():
            total[p_cat]+=value
    value = 0
    for item in list(indexes.values()):
        value += int(item[1])
    if total == {}:
        return 0
    else:
        return(total)

def get_proc_value_per_year(company,year):

    df = d[company]
    dates = list(df["Dates"])
    values = list(df["AwardedValue"])
    p_cats = list(df["ProcurementCategory"])
    winner = df["AwardedTo"]

    cat_list = {}

    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            p_cat = cleaning(d[company].iloc[i]["ProcurementCategory"])
            value = d[company].iloc[i]["AwardedValue"]
            if p_cat not in cat_list:
                cat_list[p_cat] = value
            elif p_cat in cat_list:
                cat_list[p_cat]+=value

    return(cat_list)


def get_value_year(company):
    df = d[company]
    dates = list(df["Dates"])
    values = list(df["AwardedValue"])
    p_cats = list(df["ProcurementCategory"])
    winner = df["AwardedTo"]
    year = 2013
    year_list = {2013:[],2014:[],2015:[],2016:[],2017:[],2018:[]}

    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    year+=1
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    year+=1
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    year+=1
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    year+=1
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    year+=1
    a = '01 01 ' + str(year)
    b = '31 12 ' + str(year)
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        p_cat = p_cats[i]
        if _a <= date <= _b:
            year_list[year].append(value)
    return(year_list)

box_plot = pygal.Box(box_mode="tukey", height = 300,width =600)
box_plot.title = 'Bidding Habits for ' + str(company)
year = list(get_value_year(company).keys())
values = list(get_value_year(company).values())

for i in range(len(year)):
    box_plot.add(str(year[i]), values[i])

box_plot.render_to_file('Simple_Button/pygal/'+company+'box&whisker.svg')


# Output the address for retrieval using JS
print('Simple_Button/pygal/'+company+'box&whisker.svg')

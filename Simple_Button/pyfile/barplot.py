import pandas as pd
import sys
import numpy as np
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
import pymongo
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import json
import mpld3
from mpld3 import plugins, utils
import pymongo
import re
import random
import pickle
import datetime
import pygal
from pygal.style import LightenStyle
a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
year = param['year']

try:
	agency= param['OutputFromBrowser']

except:
	agency = 1 #arbitrary


d = pickle.load(open("Simple_Button/pyfile/allagency","rb"))


def date_retrieval_all(agency, year):
    df = d[agency]
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

    else:
        return(total, value)



css = """
table
{
  border-collapse: collapse;
}
th
{
  color: #ffffff;
  background-color: #000000;
}
td
{
  background-color: #cccccc;
}
table, th, td
{
  font-family:Arial, Helvetica, sans-serif;
  border: 1px solid black;
  text-align: right;
}
"""
def to_datetime(d):
 day, month, year = map(int, d.split(' '))
 return datetime.datetime(year, month, day, 0, 0, 0)

def value_retrieval_all(agency):
    df = d[agency]
    dates = list(df["Dates"])
    values = list(df["AwardedValue"])
    p_cats = list(df["ProcurementCategory"])
    a = '01 01 2013'
    b = '31 12 2013'
    _a = to_datetime(a)
    _b = to_datetime(b)

    values_per_year = {2013:0, 2014:0, 2015:0,2016:0,2017:0,2018:0}
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:
            values_per_year[2013] += value
    a = '01 01 2014'
    b = '31 12 2014'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:
            values_per_year[2014] += value
    a = '01 01 2015'
    b = '31 12 2015'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:
            values_per_year[2015] = value
    a = '01 01 2016'
    b = '31 12 2016'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:
            values_per_year[2016] += value

    a = '01 01 2017'
    b = '31 12 2017'
    _a = to_datetime(a)
    _b = to_datetime(b)
    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:

            values_per_year[2017] += value

    a = '01 01 2018'
    b = '31 12 2018'
    _a = to_datetime(a)
    _b = to_datetime(b)

    for i in range(len(dates)):
        date = dates[i]
        value = values[i]
        if _a <= date <= _b:

            values_per_year[2018] += value



    return(values_per_year)


def bar_plots(agency,year):
    category = list(date_retrieval_all(agency,year)[0].keys())
    height = list(date_retrieval_all(agency,year)[0].values())
    dark_lighten_style = LightenStyle('#004466',title_font_size = 15, tooltip_font_size=12, label_font_size = 10 )
    line_chart = pygal.HorizontalBar(show_legend=False, style = dark_lighten_style, height = 300,width =600)
    line_chart.title = 'Total Expenditure Per Procurement Category'
    for i in range(len(category)):
        line_chart.add(category[i], height[i])

    return(line_chart.render_to_file('Simple_Button/pygal/'+agency+'bar.svg'))



bar_plots(agency,year)

print('Simple_Button/pygal/'+agency+'bar.svg')

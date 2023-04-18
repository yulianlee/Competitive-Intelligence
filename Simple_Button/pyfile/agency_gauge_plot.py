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
proc_cat =param['proc_cat']

try:
	agency= param['OutputFromBrowser']

except:
	agency = 1 #arbitrary


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
    for item in p_cats:
        if item not in values_per_year[2013]:
            values_per_year[2013][item]=[]
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
    for item in p_cats:
        if item not in values_per_year[2014]:
            values_per_year[2014][item]=[]
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
    for item in p_cats:
        if item not in values_per_year[2015]:
            values_per_year[2015][item]=[]
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
    for item in p_cats:
        if item not in values_per_year[2016]:
            values_per_year[2016][item]=[]
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
    for item in p_cats:
        if item not in values_per_year[2017]:
            values_per_year[2017][item]=[]
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
    for item in p_cats:
        if item not in values_per_year[2018]:
            values_per_year[2018][item]=[]
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

    return(values_per_year)





def gauge_plot_agency(agency, year, proc_cat):
    year = int(year)
    agency = agency
    proc_cat = proc_cat.lower()

    if proc_cat == "all":
        category = list(get_proc_cat(agency,year)['all'].keys())
        height = list(get_proc_cat(agency,year)['all'].values())


        all_vals = []

        gauge_chart = pygal.Gauge(human_readable=True,title_font_size = 1)
        gauge_chart.title = 'Agency Spending in all Procurement Categories across all years'


        for values in height:
            for i in values:
                all_vals.append(i)

        gauge_chart.range = [0, max(all_vals)]

        for i in category:
            values = get_proc_cat(agency,year)['all'][i]
            for val in values:
                gauge_chart.add(i,val)
        gauge_chart.render_to_file('Simple_Button/pygal/'+agency+'gauge_plot.svg')

    # elif proc_cat == 'current_year':
    #     values = get_proc_cat(agency,year)[year]
    #     gauge_chart = pygal.Gauge(human_readable=True, show_legend=False, height = 200,width =200,title_font_size = 1)
    #     gauge_chart.title = 'Agency Spending in all Procurement Categories in ' + str(year)
    #     all_vals = []
    #     for i in values:
    #         if i == []:
    #             continue
    #         else:
    #             all_vals.append(i)
    #     if all_vals == []:
    #
    #         gauge_chart.range = [0, 0]
    #     else:
    #         gauge_chart.range = [0, max(all_vals)]
    #
    #     for i in values:
    #         total = sum(values[i])
    #         gauge_chart.add(str(i),total)

    else:

        all_vals = []

        gauge_chart = pygal.Gauge(human_readable=True, show_legend=False,title_font_size = 1)
        gauge_chart.title = 'Agency Spending in: '+ proc_cat.upper()+ ' in ' + str(year)

        values = get_proc_cat(agency,year)[year][proc_cat]
        for i in values:
            if i == []:
                continue
            else:
                all_vals.append(i)
        if all_vals == []:

            gauge_chart.range = [0, 0]
        else:
            gauge_chart.range = [0, max(all_vals)]


        for val in values:
            gauge_chart.add(proc_cat,val)



    return(gauge_chart.render_to_file('Simple_Button/pygal/'+agency+'gauge_plot.svg'))



gauge_plot_agency(agency,year,proc_cat)

print('Simple_Button/pygal/'+agency+'gauge_plot.svg')

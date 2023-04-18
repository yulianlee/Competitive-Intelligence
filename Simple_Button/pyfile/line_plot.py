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
a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

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
    if total == {}:
        return 0
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




def line_plots(agency):
    fig, ax = plt.subplots()
    fig.set_size_inches(7,8.5)
    placeholder = list(value_retrieval_all(agency).keys())

    years = []
    for i in placeholder:
        years.append(str(i))

    y = list(value_retrieval_all(agency).values())
    lines = ax.plot(years,y, marker='o',markersize=15)


    # mpld3.plugins.connect(fig, mpld3.plugins.PointHTMLTooltip(lines[0],labels=y, css = css))

    ax.grid(True, alpha=0.3)



    df = pd.DataFrame(index=range(len(y)))
    df['Amount Spent'] = y


    labels = []
    for i in range(len(y)):
        label = df.iloc[[i], :].T
        label.columns = [years[i].format(i)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))



    ax.set_title('Total Expenditure by Year', size=20)

    tooltip = plugins.PointHTMLTooltip(lines[0], labels,voffset=10, hoffset=10, css=css)
    plugins.connect(fig, tooltip)


    json01 = json.dumps(mpld3.fig_to_dict(fig))


    return(json01)


address = 'Simple_Button/temp/'+str(agency)+'line_plot.txt'


with open(address, 'w') as outfile:
    json.dump(line_plots(agency), outfile)

print(address)

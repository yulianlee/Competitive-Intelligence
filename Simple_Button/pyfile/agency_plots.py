import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import pymongo
import re
import matplotlib.pyplot as plt  # for visualisation
import json
import collections
import sys
import matplotlib as mpl
import pickle
import mpld3
from mpld3 import plugins, utils

a = []
for line in sys.stdin:
    a.append(json.loads(line))

d = pickle.load(open("Simple_Button/pyfile/agency_dataframe","rb"))
param = json.loads(a[0])
# print(type(param))

try:
	agency = param['OutputFromBrowser']

except:
	agency = 1 #arbitrary
agency = agency.lower()

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
dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['AwardedTo'])]
dataPreProcessed = dataPreProcessed.applymap(lowerCase) # change all to lower case, preventing case sensitive

df = dataPreProcessed.reset_index()


def projs_per_agency():
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    return projs



def num_of_past_projs(agency):
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    #print(projs)
    return projs[agency]



def num_projs_graph(agency):
    z = {}
    colors = []
    projs = {}
    for i in df['Agency']:
        if i in projs:
            projs[i] += 1
        else:
            projs[i] = 1
    for num in range(1,25):
        colors.append('lightgrey')
        z[num] = 0
        for a in list(projs):
            num_projs = projs[a]
            if num_projs == num:
                z[num] += 1
    colors[projs[agency]-1]='lightcoral'
    plt.bar(range(len(z)), z.values(), align='center', color = colors)
    plt.xticks(range(len(z)), list(z.keys()))

    plt.xlabel('Number of Projects')
    plt.ylabel('Number of Agencies')
    plt.title('No. of Agencies that listed corresponding No. of Projects')

    plt.show()

    return None



def ags_projs(agency=None):
    de = df[df['Agency']==agency]
    ags_total = {}
    ags_projs = {}

    lowestbidslist = []
    awardedlowestbids = []

    for i in de.index.values: #for each project
        try:
            awardedamt = float(de.loc[i,'AwardedValue'][:-6])

            minbidamt = float(de.loc[i,'_Respondent0Value'][:-6])
            for n in range(1,17):
                if len(str(de.loc[i,'_Respondent{}Value'.format(n)])) > 3:
                    amt = float(de.loc[i,'_Respondent{}Value'.format(n)][:-6])
                    if amt < minbidamt:
                        minbidamt = amt

            lowestbidslist.append(minbidamt)
            if minbidamt == awardedamt:
                awardedlowestbids.append(minbidamt)

            if awardedamt<minbidamt:
                minbidamt = awardedamt

            maxbidamt = float(de.loc[i,'_Respondent0Value'][:-6])
            for m in range(1,17):
                if len(str(de.loc[i,'_Respondent{}Value'.format(m)])) > 3:
                    amt = float(de.loc[i,'_Respondent{}Value'.format(m)][:-6])
                    if amt > maxbidamt:
                        maxbidamt = amt

            if awardedamt>maxbidamt:
                maxbidamt = awardedamt

            if maxbidamt-minbidamt == 0:
                value = 0.5
            else:
                value = (awardedamt-minbidamt)/(maxbidamt-minbidamt)

        #values = list(value)

            projtitle = df.loc[i,'Title']

        except:
            None


        if projtitle in ags_projs:
            ags_projs[projtitle] += value
        else:
            ags_projs[projtitle] = value

    return ags_projs



def ags_avg(agency):
    return np.mean(list(ags_projs(agency).values()))


def awardminbidgraph(agency):
    a = {}
    ap = ags_projs(agency)
    minbidsawarded = 0
    for x in ap:
        if ap[x] == 0:
            minbidsawarded += 1
    minbidawardprob = minbidsawarded/len(ap)
    return minbidawardprob



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
                print(currency)



def procurement_category(agency):

    subset = df[df['Agency']==agency]
    procurement_cat = subset["ProcurementCategory"]

    return(procurement_cat)

def awarded_value(agency):
    # subset = df[df['Agency']==agency]
    # awarded_val = list(subset['AwardedValue'])
    # award_list = []
    # for item in awarded_val:
    #     cleaned = float(item.strip("(sgd) "))
    #     award_list.append(float(cleaned))
    award_list = d[agency]["AwardedValue"]
    return(award_list)

def awarded_to(agency):
    subset = df[df['Agency']==agency]
    awarded_to = list(subset['AwardedTo'])

    return(awarded_to)

# TIE THIS TO A SEPERATE PYTHON FILE TOO MANY JSONS
titles = list(ags_projs(agency).keys())
totalAwards = num_of_past_projs(agency)
probability = round(awardminbidgraph(agency)*100,2)
tendency = round(max(float(ags_avg(agency))*100,2),1)
# totalvalue = total_avg(agency)[0]
# avgvalue = total_avg(agency)[1]


# to identify procurement categories
lst= list(procurement_category(agency))

values = list(awarded_value(agency))


x_axis = list(i +1 for i in range(len(titles)))




class DragPlugin(plugins.PluginBase):
    JAVASCRIPT = r"""
    mpld3.register_plugin("drag", DragPlugin);
    DragPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    DragPlugin.prototype.constructor = DragPlugin;
    DragPlugin.prototype.requiredProps = ["id"];
    DragPlugin.prototype.defaultProps = {}
    function DragPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
        mpld3.insert_css("#" + fig.figid + " path.dragging",
                         {"fill-opacity": "1.0 !important",
                          "stroke-opacity": "1.0 !important"});
    };

    DragPlugin.prototype.draw = function(){
        var obj = mpld3.get_element(this.props.id);

        var drag = d3.behavior.drag()
            .origin(function(d) { return {x:obj.ax.x(d[0]),
                                          y:obj.ax.y(d[1])}; })
            .on("dragstart", dragstarted)
            .on("drag", dragged)
            .on("dragend", dragended);

        obj.elements()
           .data(obj.offsets)
           .style("cursor", "default")
           .call(drag);

        function dragstarted(d) {
          d3.event.sourceEvent.stopPropagation();
          d3.select(this).classed("dragging", true);
        }

        function dragged(d, i) {
          d[0] = obj.ax.x.invert(d3.event.x);
          d[1] = obj.ax.y.invert(d3.event.y);
          d3.select(this)
            .attr("transform", "translate(" + [d3.event.x,d3.event.y] + ")");
        }

        function dragended(d) {
          d3.select(this).classed("dragging", false);
        }
    }
    """

    def __init__(self, points):
        if isinstance(points, mpl.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "drag",
                      "id": utils.get_id(points, suffix)}

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
  font-size:120%;
}
"""



def agencyplot(agency):

    dataframe = d[agency]
    awards = list(dataframe["AwardedValue"])
    id_list = []


    for i in range(len(dataframe)):
        _id = dataframe.iloc[i]["_id"]
        id_list.append(_id)


    df = pd.DataFrame(index=range(len(id_list)))
    df['ID'] = [id_list[i] for i in range(len(id_list))]
    df['Awarded Value'] = [awards[i] for i in range(len(id_list))]

    labels = []

    for i in range(len(id_list)):
        label = df.iloc[[i], :].T
        label = label
        label.columns = ['Project {0}'.format(i)]
        labels.append(str(label.to_html()))

    fig, ax = plt.subplots()
    fig.set_size_inches(9, 5)
    ax.set_title(agency.upper(), fontsize=18)
    ax.set_xlabel('Individual Projects', fontsize = 15)

    points = ax.plot(awards, 'or', alpha=1,markersize=10, markeredgewidth=1, color = 'orange')

    tooltip = plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10)
    plugins.connect(fig, DragPlugin(points[0]))
    plugins.connect(fig, tooltip)
    json01 = json.dumps(mpld3.fig_to_dict(fig))
    return(json01)

# def agencyplot(agency):
#     fig, ax = plt.subplots()
#     # fig.set_size_inches(5, 4)
#     ax.set_title(agency.upper(), fontsize=18)
#     # ax.set_ylabel('Awarded Project Values', fontsize = 15)
#     ax.set_xlabel('Individual Projects', fontsize = 15)
#
#     points = ax.plot(values, 'or', alpha=0.5,markersize=10, markeredgewidth=1, color = 'orange')
#
#
#     # tooltip = plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10, css=css)
#     # plugins.connect(fig, tooltip)
#     plugins.connect(fig, DragPlugin(points[0]))
#
#
#     json01 = json.dumps(mpld3.fig_to_dict(fig))
#
#
#     return(json01)


address = 'Simple_Button/temp/'+str(agency)+'.txt'


with open(address, 'w') as outfile:
    json.dump(agencyplot(agency), outfile)

print(address)

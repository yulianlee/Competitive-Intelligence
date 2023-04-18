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


a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])

outcome = param["outcome"]
# print(type(param))

try:
	company = param['OutputFromBrowser']


except:
	company = 1 #arbitrary


myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
mydb = myclient["gebizz"]  #DB name
mycol = mydb["GeBizCollection"]  #Collection name

#Select only IT Service 408 entries out of 11k
myquery = {}  #Query  -- can change

#ProcurementCategory
mydoc = mycol.find(myquery)
data = []
for x in mydoc:
    data.append(x)
# data = pickle.load(open("./pyfile/all_stuff","rb"))
for entry in data:
    if len(entry['Awards']) == 1:
        for i in range(len(entry['Respondents'])):
            entry[('Respondent'+str(i))] = entry['Respondents'][str(i)]['CompanyName']
            entry[('_Respondent'+str(i)+"Value")] = entry['Respondents'][str(i)]['TotalPrice']
        entry['AwardedTo'] = entry['Awards'][str(0)]['AwardedTo']
        entry['AwardedValue'] = entry['Awards'][str(0)]['AwardedValue']
        pass


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
# dataPreProcessed = dataPreProcessed["ProcurementCategory"].apply(cleaning)
dataPreProcessed = dataPreProcessed.applymap(lowerCase) # change all to lower case, preventing case sensitive


def convertToSGD(string):
    if isinstance(string, str):
        x = string.split("(")
        amount = float(x[0])
        currency = x[1].strip()
        currency = currency[:-1]

        exchangeRate = {'sgd':1,'usd':1.36032,'eur':1.52292,'myr':0.32874,'chf':1.33804,'gbp':1.76,'aud':1.07, 'sek':6.96,
                       'nzd':1.12, 'qar':2.64, 'cnh':5.12,'bnd':1,'jpy':76.84,'aed':2.66,'idr':10282.09, 'php':37.78,'cad':0.96,
                       'inr':51.29}
        if currency in exchangeRate:
            sgdValue = amount * exchangeRate[currency]
        else:
            sgdValue = 0
        return float(sgdValue)

maxRespondent = len(list(dataPreProcessed.filter(regex="^Resp")))

for i in range(maxRespondent):
    dataPreProcessed['_Respondent'+str(i)+'Value'] = dataPreProcessed['_Respondent'+str(i)+'Value'].apply(convertToSGD)
dataPreProcessed['AwardedValue'] = dataPreProcessed['AwardedValue'].apply(convertToSGD)
# dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['Agency'])]
# dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['AwardedDate'])]
# dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['NoOfSuppliersAwarded'])]
# dataPreProcessed = dataPreProcessed[pd.notnull(dataPreProcessed['ProcurementCategory'])]

dataPreProcessed= dataPreProcessed.reset_index()
del dataPreProcessed["index"]


def no_of_bids(company):
    competitorlist = {}
    for i in range(len(dataPreProcessed["Agency"])):
        for j in range(0,42):
            try:
                name = dataPreProcessed["Respondent"+str(j)][i]
                if name not in competitorlist:
                    competitorlist[name]=1
                else:
                    competitorlist[name]+=1
            except:
                pass
    return competitorlist[company]

# no_of_bids("led signs pte. ltd.")


#projectdic = {project:{competitor:bidamt}}
titles = []
for i in range(len(dataPreProcessed["Agency"])):
    try:
        if np.isnan(dataPreProcessed['AwardedValue'][i])==False:
            titles.append(dataPreProcessed['Title'][i])
    except:
        pass

# print(len(titles))

# initialize a dictionary using the all the titles, values are respondents and their bidded amounts
projectdic = dict.fromkeys(titles, 0)

for i in range(len(dataPreProcessed["Agency"])):
    try:
        a = {}
        for j in range(0,42):
            try:
                if np.isnan(dataPreProcessed["Respondent"+str(j)][i])==True:
                    pass
            except:
                a[dataPreProcessed["Respondent"+str(j)][i]]=dataPreProcessed['_Respondent'+str(j)+'Value'][i]
        projectdic[dataPreProcessed['Title'][i]]=a
    except:
        pass
# print(projectdic)


#minmax & biddiff
#minmax = indexing the highest and lowest bid
#biddiff = difference in the highest and lowest bid
minmax = {}
mmdiff = {}
for pj in projectdic:
    minbid = 10000000000000000
    maxbid = 0
    for bid in projectdic[pj]:
        if projectdic[pj][bid]<minbid:
            minbid = projectdic[pj][bid]
        if projectdic[pj][bid]>maxbid:
            maxbid = projectdic[pj][bid]
    minmax[pj] = [minbid,maxbid]
    mmdiff[pj] = maxbid-minbid

companiesdic = pickle.load(open("Simple_Button/pyfile/companies_dict","rb"))
competitors = pickle.load(open("Simple_Button/pyfile/competitors_stored","rb"))
#competitors = {company:{project:diff}}
bidcount = pickle.load(open("Simple_Button/pyfile/bidcount_stored","rb"))
#bidcount = {company:no. of bids}
wincount = pickle.load(open("Simple_Button/pyfile/wincount_stored","rb"))
#wincount = {company:no. of wins}
competitorpjs = pickle.load(open("Simple_Button/pyfile/competitorpjs_stored","rb"))
#competitorpjs = {company:[projects]}
totalbids = pickle.load(open("Simple_Button/pyfile/totalbids_stored","rb"))
#totalbids = {company: total bidded amount for all projects}
index = pickle.load(open("Simple_Button/pyfile/index_stored","rb"))
# index = {company:{project:bid index}}

def date(company,project):
    return companiesdic[company][project][0]

def title(company,project):
    return companiesdic[company][project][1]

def bidamt(company,project):
    return companiesdic[company][project][2]

def awardval(company,project):
    return companiesdic[company][project][3]

def diff(company,project):
    return companiesdic[company][project][4]

def indexval(company,project):
    return companiesdic[company][project][5]

def procurement_cat(company,project):
    return companiesdic[company][project][6]


def avgbidindex(company):
    totalindex = 0
    for proj in index[company]:
        totalindex += index[company][proj]
    avgindex = totalindex/no_of_bids(company)
    return avgindex



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



fig, ax = plt.subplots()
# fig.set_size_inches(5, 4)
ax.set_title(company.upper(), fontsize=18)
# ax.set_ylabel('Bid Value Difference', fontsize = 15)
ax.set_xlabel('Individual Projects', fontsize = 15)

limit=[]
for value in list(competitors[company].values()):
    val = abs(value)
    limit.append(val)
plt.ylim(-(max(limit)+max(limit)/10),(max(limit)+max(limit)/10))



x = list(competitors[company].keys())
y = list(competitors[company].values())

selectedcomp = companiesdic[company]
proj_details = list(selectedcomp.values())
titles = list(selectedcomp.keys())


date_list = []
bidamt_list = []
awardedval_list = []
diff_list = []
indexval_list = []
id_list = []
winner_list = []
awarded_to = []
proc_list = []

for i in range(len(proj_details)):
    date = proj_details[i][0]
    bidamt = proj_details[i][2]
    awardedval = proj_details[i][3]
    diff = proj_details[i][4]
    index_val = proj_details[i][5]
    ID = proj_details[i][8]
    winner = proj_details[i][7]
    proc_cat = proj_details[i][6]

    date_list.append(date)
    bidamt_list.append(bidamt)
    awardedval_list.append(awardedval)
    diff_list.append(diff)
    indexval_list.append(index_val)
    id_list.append(ID)
    awarded_to.append(winner)
    proc_list.append(proc_cat)

    if winner == company:
        winner_list.append("Won Tender Bid")
    else:
        winner_list.append("Lost Tender Bid")

# doubled = [thing for thing in list_of_things]
df = pd.DataFrame(index=range(len(x)))
df['Project Title'] = [x[i] for i in range(len(x))]
df['Bid Amount Difference'] = [str(y[i]) for i in range(len(y))]
df['Awarded Date'] = [date_list[i] for i in range(len(date_list))]
df['Bidded Amount']  = [str(bidamt_list[i]) for i in range(len(bidamt_list))]
df['Awarded Amount'] = [str(awardedval_list[i]) for i in range(len(awardedval_list))]
df['Bid Difference']  = [str(indexval_list[i]) for i in range(len(indexval_list))]
df['Project ID']  = [id_list[i] for i in range(len(id_list))]
df['Outcome of Bid']  = [winner_list[i] for i in range(len(winner_list))]
df['Procurement Category']  = [proc_list[i] for i in range(len(proc_list))]


labels = []
for i in range(len(x)):
    label = df.iloc[[i], :].T
    label.columns = ['Project {0}'.format(i)]
    # .to_html() is unicode; so make leading 'u' go away with str()
    labels.append(str(label.to_html()))


limit=[]
for value in list(competitors[company].values()):
    val = abs(value)
    limit.append(val)
plt.ylim(-(max(limit)+max(limit)/10),(max(limit)+max(limit)/10))



x = list(competitors[company].keys())
y = list(competitors[company].values())

selectedcomp = companiesdic[company]
proj_details = list(selectedcomp.values())
winner_list = []
losing_list = []

for i in range(len(proj_details)):
        date = proj_details[i][0]
        bidamt = proj_details[i][2]
        awardedval = proj_details[i][3]
        diff = proj_details[i][4]
        index_val = proj_details[i][5]
        ID = proj_details[i][6]
        winner = proj_details[i][7]

        date_list.append(date)
        bidamt_list.append(bidamt)
        awardedval_list.append(awardedval)
        diff_list.append(diff)
        indexval_list.append(index_val)
        id_list.append(ID)

        if winner == company:
            winner_list.append(bidamt)

        else:
            losing_list.append(bidamt)


def comp_outcome(outcome):
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    labels_new = []
    if outcome == "WON":
        points = ax.plot(winner_list, 'or', alpha=1,markersize=12, markeredgewidth=1, color = 'red')
        for i in range(len(df)):
            if df.iloc[i]["Outcome of Bid"] == "Won Tender Bid":
                label = df.iloc[[i], :].T
                label.columns = ['Project {0}'.format(i)]
                labels_new.append(str(label.to_html()))
    elif outcome == "LOST":
        points = ax.plot(losing_list, 'or', alpha=1,markersize=12, markeredgewidth=1, color = 'black')
        for i in range(len(df)):
            if df.iloc[i]["Outcome of Bid"] == "Lost Tender Bid":
                label = df.iloc[[i], :].T
                label.columns = ['Project {0}'.format(i)]
                labels_new.append(str(label.to_html()))
    elif outcome == 'ALL':

        points = ax.plot(y, 'or', alpha=0.7,markersize=12, markeredgewidth=1, color = 'orange')

        labels_new = labels


    tooltip = plugins.PointHTMLTooltip(points[0], labels_new, voffset=10, hoffset=10, css=css)
    plugins.connect(fig, tooltip)
    plugins.connect(fig, DragPlugin(points[0]))
    json01 = json.dumps(mpld3.fig_to_dict(fig))


    return(json01)


address = 'Simple_Button/temp/'+str(company)+'plots.txt'


with open(address, 'w') as outfile:
    json.dump(comp_outcome(outcome), outfile)

print(address)

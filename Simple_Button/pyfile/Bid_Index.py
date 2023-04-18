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


a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	company = param['OutputFromBrowser']
except:
	company = 1 #arbitrary


# myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
# mydb = myclient["gebizz"]  #DB name
# mycol = mydb["GeBizCollection"]  #Collection name
#
# #Select only IT Service 408 entries out of 11k
# myquery = {'ProcurementCategory': 'IT&Telecommunication ⇒ IT Services & Software Development '}  #Query  -- can change
#
# #ProcurementCategory
# mydoc = mycol.find(myquery)
# data = []
# for x in mydoc:
#     data.append(x)
data = pickle.load(open("./pyfile/all_stuff","rb"))
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
dataPreProcessed = dataPreProcessed.applymap(lowerCase) # change all to lower case, preventing case sensitive

def convertToSGD(string):
    if isinstance(string, str):
        x = string.split("(")
        amount = float(x[0])
        currency = x[1].strip()
        currency = currency[:-1]

        exchangeRate = {'sgd':1,'usd':1.36032,'eur':1.52292,'myr':0.32874,'chf':1.33804,'gbp':1.76}

        sgdValue = amount * exchangeRate[currency]
        return sgdValue

maxRespondent = len(list(dataPreProcessed.filter(regex="^Resp")))

for i in range(maxRespondent):
    dataPreProcessed['_Respondent'+str(i)+'Value'] = dataPreProcessed['_Respondent'+str(i)+'Value'].apply(convertToSGD)
dataPreProcessed['AwardedValue'] = dataPreProcessed['AwardedValue'].apply(convertToSGD)

dataPreProcessed['MeanBid'] = dataPreProcessed.filter(regex="^_Resp").mean(axis=1)

for i in range(maxRespondent):
    dataPreProcessed['Differences'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['AwardedValue']
    dataPreProcessed['_DifferencesFromMean'+str(i)] = dataPreProcessed['_Respondent'+str(i)+'Value'] - dataPreProcessed['MeanBid']
dataPreProcessed = dataPreProcessed.sort_values(by=['AwardedValue'],ascending=True)



#number of projects = competitorlist[company1]
def no_of_bids(company):
    competitorlist = {}
    for i in range(0,408):
        for j in range(0,17):
            try:
                name = dataPreProcessed["Respondent"+str(j)][i]
                if name not in competitorlist:
                    competitorlist[name]=1
                else:
                    competitorlist[name]+=1
            except:
                pass
    return competitorlist[company]




#projectdic = {project:{competitor:bidamt}}
titles = []
for i in range(0,408):
    try:
        if np.isnan(dataPreProcessed['AwardedValue'][i])==False:
            titles.append(dataPreProcessed['Title'][i])
    except:
        pass

projectdic = dict.fromkeys(titles, 0)

for i in range(0,408):
    try:
        a = {}
        for j in range(0,17):
            try:
                if np.isnan(dataPreProcessed["Respondent"+str(j)][i])==True:
                    pass
            except:
                a[dataPreProcessed["Respondent"+str(j)][i]]=dataPreProcessed['_Respondent'+str(j)+'Value'][i]
        projectdic[dataPreProcessed['Title'][i]]=a
    except:
        pass



#minmax & biddiff
minmax = {}
mmdiff = {}
for pj in projectdic:
    minbid = 1000000000
    maxbid = 0
    for bid in projectdic[pj]:
        if projectdic[pj][bid]<minbid:
            minbid = projectdic[pj][bid]
        if projectdic[pj][bid]>maxbid:
            maxbid = projectdic[pj][bid]
    minmax[pj] = [minbid,maxbid]
    mmdiff[pj] = maxbid-minbid


competitors = {}
#competitors = {company:{project:diff}}
bidcount = {}
#bidcount = {company:no. of bids}
wincount = {}
#wincount = {company:no. of wins}
competitorpjs = {}
#competitorpjs = {company:[projects]}
totalbids = {}
#totalbids = {company: total bidded amount for all projects}
index = {}
#index = {company:{project:bid index}}
companiesdic = {}
#companiesdic = {company:{project:[date,title,bidamt,awardval,diff,indexval]}}

for i in range(0,408):
    for j in range(0,17):
        try:
            name = dataPreProcessed["Respondent"+str(j)][i]
            project = dataPreProcessed['Title'][i]
            bid = dataPreProcessed['_Respondent'+str(j)+'Value'][i]
            diff = bid - dataPreProcessed['AwardedValue'][i]
            ID = dataPreProcessed['QuotationNo'][i]

            if name not in competitors:
                competitors[name]={project:diff}
            else:
                competitors[name][project]=diff
            if name not in bidcount:
                bidcount[name]=1
            else:
                bidcount[name]+=1
            if name not in wincount:
                if diff == 0:
                    wincount[name]=1
                else:
                    wincount[name]=0
            else:
                if diff == 0:
                    wincount[name]+=1
            if name not in competitorpjs:
                competitorpjs[name]=[project]
            else:
                competitorpjs[name].append(project)
            if name not in totalbids:
                totalbids[name]=bid
            else:
                totalbids[name]+=bid

            if mmdiff[project]>0:
                bidindex=(bid-(float(minmax[project][0])))/(mmdiff[project])
            else:
                bidindex=0.5
            if name not in index:
                index[name]={project:bidindex}
            else:
                index[name][project]=bidindex

            if name not in companiesdic:
                companiesdic[name]={project:[dataPreProcessed['TenderClosingDate'][i],project,bid,dataPreProcessed['AwardedValue'][i],diff,bidindex, ID]}
            else:
                companiesdic[name][project]=[dataPreProcessed['TenderClosingDate'][i],project,bid,dataPreProcessed['AwardedValue'][i],diff,bidindex, ID]


        except:
            pass


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



def avgbidindex(company):
    totalindex = 0
    for proj in index[company]:
        totalindex += index[company][proj]
    avgindex = totalindex/no_of_bids(company)
    return avgindex



winrate = {k: wincount[k] / float(bidcount[k]) for k in bidcount if k in wincount}


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

#BID INDEX PLOT (company)
def indexplot(company):

    x = list(index[company].keys())
    y = list(index[company].values())

    label = [''*len(index[company].keys())]

    df = pd.DataFrame(index=range(len(x)))
    df['Project Title'] = [x[i] for i in range(len(x))]
    df['Bid Index Difference'] = [y[i] for i in range(len(y))]

    labels = []
    for i in range(len(x)):
        label = df.iloc[[i], :].T
        label.columns = ['Project {0}'.format(i)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))

    fig2, ax2 = plt.subplots()
    fig2.set_size_inches(5, 4)
    ax2.set_title(company, fontsize=18)
    ax2.set_ylabel('Bid Index Difference', fontsize = 15)
    ax2.set_xlabel('Individual Projects', fontsize = 15)


    points2 = ax2.plot(y, 'or', alpha=1,markersize=7.5, markeredgewidth=1, color = 'orange')


    tooltip = plugins.PointHTMLTooltip(points2[0], labels, voffset=10, hoffset=10, css=css)
    plugins.connect(fig2, tooltip)
    plugins.connect(fig2, DragPlugin(points2[0]))



    json02 = json.dumps(mpld3.fig_to_dict(fig2))
    return (json02)


address2 = './temp/'+str(company)+'2'+'.txt'

with open(address2, 'w') as outfile:
    json.dump(indexplot(company), outfile)

print(address2)

import sys
import json
from algo import prediction
from value_prediction import get_value,get_similar_sentence
from company_analysis import bid_range,win_rate,total_sum,plot_difference_from_mean
from consolidatedforUI import num_of_past_projs,total_avg,awardminbidgraph,ags_avg,ags_projs,procurement_category
import pymongo
import re
import random

a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	agency = param['OutputFromBrowser']

except:
	agency = 1 #arbitrary

#
# agency = arguments.lower()
totalAwards = num_of_past_projs(agency)
totalValue = total_avg(agency)[0]
avgValue = total_avg(agency)[1]
pLowest = round(awardminbidgraph(agency)*100,2)
tendancy = round(max(float(ags_avg(agency))*100,2),1)
result = total_avg(agency)[2]
procurement = procurement_category(agency)

def agency_details(agency):
    dict = {"totalAwards":totalAwards,"totalValue":totalValue,"avgValue":avgValue,"pLowest":pLowest,"tendency":tendancy,'data':result, 'procurement':procurement}
    return json.dumps(dict)


# Create address variable in the temp folder
address = 'Simple_Button/temp/'+str(agency)+"details"+'.txt'


with open(address, 'w') as outfile:
    json.dump(agency_details(agency), outfile)

print(address)

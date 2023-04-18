import sys
import json
from algo import prediction
from value_prediction import get_value,get_similar_sentence
#from getNames import getNameList
from company_analysis import bid_range,win_rate,total_sum,plot_difference_from_mean
from consolidatedforUI import num_of_past_projs,total_avg,awardminbidgraph,ags_avg,ags_projs
import pymongo
import re
import random
import pickle


a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))
method = param['action']
try:
	arguments = param['OutputFromBrowser']
except:
	arguments = 1 #arbitrary


def title_detail(arguments):
	companies = prediction(arguments)
	topics = get_similar_sentence(arguments)
	value = get_value(arguments)[0]
	MAE = get_value(arguments)[1]
	dict1 = {"title":arguments ,"topics":topics,"companies":companies,"value":value,"MAE":MAE}
	return json.dumps(dict1)



def return_value(method,arguments=None):
    switcher = {
        "titleSearch": title_detail

    }
    # Get the function from switcher dictionary
    func = switcher.get(method)
    # Execute the function
    # return func(arguments)

# this is a temporary file with random integer suffix
address = 'Simple_Button/temp/'+'title_search'+str(random.randint(1,10000001))+'.txt'

with open(address, 'w') as outfile:
    json.dump(title_detail(arguments), outfile)

print(address)

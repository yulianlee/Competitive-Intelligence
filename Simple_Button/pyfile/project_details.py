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


a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))
method = param['action']
try:
	arguments = param["title"]
except:
	arguments = 1 #arbitrary


def project_detail(arguments):
	'''
	Direct query into MongoDB for a particular project
	using regex
	'''
	types = arguments['type']
	query = arguments['query']
	exact = int(arguments['exact'])

	try:
		num = int(arguments['num'])
	except:
		num = 5

	myclient = pymongo.MongoClient("mongodb://localhost:27017/") #Port
	mydb = myclient["gebizz"]  #DB name
	mycol = mydb["GeBizCollection"]  #Collection name
	myquery = {}

	if exact == 0:
		query = query.replace("(","\\(").replace(")","\\)").replace("/","\\/")
		myquery[types] = re.compile(query, re.IGNORECASE)
	else:
		myquery[types] = query
	mydoc = mycol.find(myquery).limit(num)
	data = []
	for x in mydoc:
		data.append(x)
	return json.dumps(data)



def return_value(method,arguments=None):
    switcher = {
        "projectSearch": project_detail

    }
    # Get the function from switcher dictionary
    func = switcher.get(method)
    # Execute the function
    # return func(arguments)

# this is a temporary file with random integer suffix
address = 'Simple_Button/temp/'+'project_search'+str(random.randint(1,10000001))+'.txt'

with open(address, 'w') as outfile:
    json.dump(project_detail(arguments), outfile)

print(address)

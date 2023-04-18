import sys
import json
import pymongo
import re
import random

a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	arguments = param['OutputFromBrowser']

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


# Create address variable in the temp folder
address = 'Simple_Button/temp/'+"dbsearch"+''+str(random.randint(1,10000001))+'.txt'

# Write a file to the address
with open(address, 'w') as outfile:
	json.dump(project_detail(arguments), outfile)

# Output the address for retrieval using JS
print(address)

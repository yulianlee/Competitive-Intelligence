import sys
import json
from company_analysis import bid_range,win_rate,total_sum,plot_difference_from_mean, get_FG
import pymongo
import re
import random


a = []
for line in sys.stdin:
    a.append(json.loads(line))

# inputs in the form of [{["a":"1"]}]

# read first (and only) variable in the list a
param = json.loads(a[0])


# retrieve arguments for the function
try:
	arguments = param['OutputFromBrowser']
except:
	arguments = 1 #arbitrary

# def get_FG(company):
#     award = 0
#     for i in range(len(d[company])):
#         value = d[company]["AwardedValue"].max()
#
#     if value<= 100000:
#         FG = "S2'"
#     elif 100000< value <= 250000:
#         FG = "S3"
#     elif 250000< value <= 500000:
#         FG = "S4"
#     elif 500000< value <= 1000000:
#         FG = "S5"
#     elif 1000000< value <= 3000000:
#         FG = "S6"
#     elif 3000000< value <= 5000000:
#         FG = "S7"
#     elif 5000000< value <= 10000000:
#         FG = "S8"
#     elif 10000000< value <= 30000000:
#         FG = "S9"
#     elif 30000000< value:
#         FG = "S10"
#     return (FG)
#
# def company_detail(arguments):
#
# 	comp = arguments
# 	bidRange = bid_range(comp)
# 	winRate = win_rate(comp)
# 	totalSum = total_sum(comp)
# 	dict1 = {"title":arguments ,"bidRange":bidRange,"winRate":winRate,"totalSum":totalSum}
# 	return json.dumps(dict1)

def company_detail(arguments):
    comp = arguments
    fg = get_FG(comp)
    bidRange = bid_range(comp)
    winRate = win_rate(comp)
    totalSum = total_sum(comp)
    dict1 = {"title":arguments ,"bidRange":bidRange,"winRate":winRate,"totalSum":totalSum,"fg":fg}
    return json.dumps(dict1)
# Create address variable in the temp folder
address = 'Simple_Button/temp/'+arguments+'company_details'+''+str(random.randint(1,10000001))+'.txt'

# Write a file to the address
with open(address, 'w') as outfile:
	json.dump(company_detail(arguments), outfile)

# Output the address for retrieval using JS
print(address)

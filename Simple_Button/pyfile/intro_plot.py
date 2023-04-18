import sys
import json
import pymongo
import re
import random
import pandas as pd   # pandas for data frame organization
import numpy as np  # numpy for math stuff
import collections
import pickle
from collections import Counter
import pygal
from pygal.style import Style
a = []
for line in sys.stdin:
    a.append(json.loads(line))


param = json.loads(a[0])
# print(type(param))

try:
	category = param['OutputFromBrowser']

except:
	category = 1 #arbitrary


def top_3_by_value(category):
    d= pickle.load(open("Simple_Button/pyfile/dictionary_dataframe_2","rb"))
    for item in d.keys():
        if category == item:
            dataframe = d[str(category)]
        # else:
        #     return (json.dumps("ERROR"))
    awarded_vals = dataframe["AwardedValue"]

    custom_style = Style(
      tooltip_font_size=30 ,opacity_hover=0.1, title_font_size = 30, font_family='Poppins')

    pie_chart = pygal.Pie(inner_radius=.75, show_legend=False, style = custom_style, title=str(category.upper()))
    for i in range(len(list(dataframe["Title"]))):
    #    pie_chart.add("Project ID:"+'\n'+str(dataframe.iloc[i]["_id"])+'\n'+'\n'+'\n'+"Awarded Value is:"+'\n'+str(dataframe.iloc[i]["AwardedValue"]), float(dataframe.iloc[i]["AwardedValue"]/total_value))
        pie_chart.add("Project ID:"+'\n'+str(dataframe.iloc[i]["_id"])+'\n'+'\n'+"Agency:"+'\n'+str(dataframe.iloc[i]["Agency"].upper()),(float(dataframe.iloc[i]["AwardedValue"])))

    pie_chart.render_to_file('Simple_Button/pygal/'+category+'.svg')

    return(pie_chart.render_to_file('Simple_Button/pygal/'+category+'.svg'))



# Output the address for retrieval using JS
print('Simple_Button/pygal/'+category+'.svg')

# C:\Users\Lee Ying Hern\Desktop\Simple Button2\Simple Button\pygal\services advertising services.svg
# address = './temp/'+"intro_page"+''+str(random.randint(1,10000001))+'.txt'
#
# # Write a file to the address
# with open(address, 'w') as outfile:
# 	json.dump(top_3_by_value(category), outfile)
#
# # Output the address for retrieval using JS
# print(address)

top_3_by_value(category)

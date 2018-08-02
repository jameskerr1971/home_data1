import re
import time
from datetime import datetime
#from pymongo import MongoClient
import pymongo

#wait for the scraper script to run at the start of the minute
time.sleep(10)

connection = pymongo.MongoClient('mongodb://192.168.0.53/')
db = connection.web

#get the data from the scrapings file
with open ('/home/dennett/scripting/Scrapings_RochTemp.txt', 'rt') as in_file:
    contents = in_file.read()

#CPU PERCENT
roch_temp_digits = []
roch_temp_mo = re.search('(report_text temperature)...............................', contents)
roch_temp_text = roch_temp_mo.group()
print('roch_temp_text ', roch_temp_text)
roch_temp_digits_list = re.findall('\d+\.?\d*', roch_temp_text)
print('roch_temp_digits_list ', roch_temp_digits_list)
roch_temp_digits = roch_temp_digits_list[2]
roch_temp =  int(roch_temp_digits)

#use UTC time to avoid BST changes
now = datetime.utcnow()
t = now.isoformat()

roch_temp_data_dict = {'Time': t, 'Metric': roch_temp}

print('roch_temp_data_dict ', roch_temp_data_dict)
roch_temp_coll = db.rochester_temp
roch_temp_write = roch_temp_coll.insert_one(roch_temp_data_dict)

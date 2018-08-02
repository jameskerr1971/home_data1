import re
import time
from datetime import datetime
#from pymongo import MongoClient
import pymongo

#wait for the scraper script to run at the start of the minute
time.sleep(40)

#get the data from the scrapings file
with open ('/home/dennett/scripting/Scrapings_Popper.txt', 'rt') as in_file:
    contents = in_file.read()

cpu_percent_digits = []

cpu_percent_digits_list = re.findall('\d+\.?\d*', contents)

#print('cpu_percent_digits_list', cpu_percent_digits_list)

cpu_percent_int_list = []

for i in cpu_percent_digits_list:
    f = int(i)
    cpu_percent_int_list.append(f)

#print('cpu_percent_int_list ', cpu_percent_int_list)

cpu_percent_int = sum(cpu_percent_int_list) / float(len(cpu_percent_int_list))

#print('cpu_percent_int ', cpu_percent_int)

#use UTC time to avoid BST changes
now = datetime.utcnow()
t = now.isoformat()

data_dict = {'Time': t, 'Metric': cpu_percent_int}

#print(data_dict)

connection = pymongo.MongoClient('mongodb://192.168.0.53/') 
db = connection.device
coll = db.popper_cpu

result = coll.insert_one(data_dict)

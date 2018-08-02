import re
import time
from datetime import datetime
import pymongo
import pycurl
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

def run_curl(url, coll):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    curl_response_time_seconds = c.getinfo(c.TOTAL_TIME)
#times by 1000 for milliseconds
    curl_response_time = curl_response_time_seconds * 1000
    print('curl_response_time ', curl_response_time)
#print(type(curl_response_time))

# getinfo must be called before close.
    c.close()

    now = datetime.utcnow()
#isoformat (which includes the "T" in the middle
    now_iso = now.isoformat()
    now_iso_str = str(now_iso)
    t = now.isoformat()

    data_dict = {'Time': t, 'Metric': curl_response_time}
#print(data_dict)
    connection = pymongo.MongoClient('mongodb://192.168.0.53') 
    connect_db = connection.curl
    connect_db_coll = connect_db[coll]
    result = connect_db_coll.insert_one(data_dict)

skyrouter = run_curl('http://192.168.0.1', 'skyrouter_response')
viavidotcom = run_curl('http://www.viavisolutions.com', 'viavidotcom_response')

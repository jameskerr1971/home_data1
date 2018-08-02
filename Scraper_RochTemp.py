#from bs4 import BeautifulSoup
import requests

#Data source
url = 'https://www.worldweatheronline.com/rochester-weather/kent/gb.aspx'

#Get data
r = requests.get(url)
#soup = BeautifulSoup(r.text, 'lxml')

response_text = r.text

encoded_text = response_text.encode('utf-8')

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in response_text.splitlines())

# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

# drop blank lines
tidy_text = '\n'.join(chunk for chunk in chunks if chunk)

# remove whitespace
tidier_text = "".join(line.strip() for line in tidy_text.split("\n"))

#print(tidier_text)

#Write data
f = open('/home/dennett/scripting/Scrapings_RochTemp.txt', 'w')
f.write(tidier_text)

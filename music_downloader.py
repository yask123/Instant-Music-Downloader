# /usr/local/bin/python

import os
import glob
from bs4 import BeautifulSoup
import urllib2
from urllib import quote_plus as qp

search = 'love story taylor' #I love you Taylor swift!
search = raw_input('Enter songname/ lyrics/ artist.. or whatever ')
search = qp(search)

print('Making a Query Request! ')
response = urllib2.urlopen('https://www.youtube.com/results?search_query='+search)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')
for link in soup.find_all('a'):
    if '/watch?v=' in link.get('href'):
    	print(link.get('href'))
    	# May change when Youtube Website may get updated in the future.
    	proper_linl = link.get('href')
    	break
 
proper_linl =  'http://www.youtube.com/'+proper_linl
command = 'youtube-dl --extract-audio --audio-format mp3 '+proper_linl
print ('Processed Querying , Starting Phase 2')
os.system(command)




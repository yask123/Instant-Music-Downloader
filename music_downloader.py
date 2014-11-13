import os
import glob

import urllib2
intro_art = """
 \ \   / /      | |  ( )     |  \/  |         (_)      |  __ \                    | |               | |          
  \ \_/ /_ _ ___| | _|/ ___  | \  / |_   _ ___ _  ___  | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
   \   / _` / __| |/ / / __| | |\/| | | | / __| |/ __| | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
    | | (_| \__ \   <  \__ \ | |  | | |_| \__ \ | (__  | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
    |_|\__,_|___/_|\_\ |___/ |_|  |_|\__,_|___/_|\___| |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|  
"""
print (intro_art)
choice = 'Y'
while(choice == 'Y'):
	try :
		search = 'love story taylor' # Test Case 
		search = testVar = raw_input("Enter Song Name\n")

		search = search.replace(' ','%20')
		print('Making a Query Request! ')
		response = urllib2.urlopen('https://www.youtube.com/results?search_query='+search)
		html = response.read()
		a =html.find('<h3 class="yt-lockup-title"><a href="/watch?')
		raw_link= (html[a+43:a+57]) # May change when Youtube Website may get updated in the future.
		proper_linl = 'https://www.youtube.com/watch'+raw_link


		command='youtube-dl -t --format bestaudio '+proper_linl
		print ('Processed Querying , Starting Phase 2')
		os.system(command)

		choice = raw_input('Download Another music Y/N ?')
	except :
		print ('Sorry , An error eccored , please report the Bug')	


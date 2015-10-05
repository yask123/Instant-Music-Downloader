#!/usr/bin/env python

import os
import glob
from bs4 import BeautifulSoup


# Version compatiblity
import sys
if (sys.version_info > (3,0)):
	from urllib.request import urlopen
	from urllib.parse import quote_plus as qp
	raw_input = input
else:
	from urllib2 import urlopen
	from urllib import quote_plus as qp


# Define query and download code.
def query_and_download(search, has_prompts=True, is_quiet=False):
    
    if not is_quiet:
        print('Making a Query Request! ')

    # Magic happens here.
    response = urlopen('https://www.youtube.com/results?search_query=' + search)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if '/watch?v=' in link.get('href'):
    	    # May change when Youtube gets updated in the future.
    	    video_link = link.get('href')
    	    break

    title = soup.find("a", "yt-uix-tile-link").text

    if not is_quiet:
        print("Found: " + title)
    if has_prompts:
        prompt = raw_input("Download song (y/n)? ")
        if prompt != "y":
            sys.exit()

    # Links are relative on page, making them absolute.
    video_link = 'http://www.youtube.com/' + video_link
    if is_quiet:
        command = 'youtube-dl -q --extract-audio --audio-format mp3 --audio-quality 0 ' + video_link
    else:
        command = 'youtube-dl --extract-audio --audio-format mp3 --audio-quality 0 ' + video_link
     

    # Youtube-dl is a proof that god exists.
    if not is_quiet:
        print ('Downloading...')
    os.system(command)


# Run script
search = ''
# No command-line arguments
if not sys.argv[1:]:
    # We do not want to accept empty inputs :)
    while search == '':
        search = raw_input('Enter songname/ lyrics/ artist.. or whatever\n> ')
        search = qp(search)
    query_and_download(search)

# Call from command line!
else:
    # No flag
    if sys.argv[1][0] != '-':
        search = qp(' '.join(sys.argv[1:]))
        query_and_download(search)

    # Flag provided
    else:
        # Lots of parser-building fun
        import argparse
        parser = argparse.ArgumentParser(description='Instantly download any song!')
        parser.add_argument('-p', action='store_false', dest='has_prompt', help="Turn off download prompts")
        parser.add_argument('-q', action='store_true', dest='is_quiet', help="Run in quiet mode")
        parser.add_argument('-s', action='store', dest='song', nargs='+', help='Download a single song.')
        parser.add_argument('-l', action='store', dest='songlist', nargs='+', help='Download a list of songs, with lyrics separated by a comma (e.g. "i tried so hard and got so far, blackbird singing in the dead of night, hey shawty it\'s your birthday).')
        parser.add_argument('-f', action='store', dest='file', nargs='+', help='Download a list of songs from a file input. Each line in the file is considered one song.')

        # Parse and check arguments
        results = parser.parse_args()

        songs_list = []
        if results.song:
            songs_list.append(qp(' '.join(results.song)))

        if results.songlist:
            songs = ' '.join(results.songlist)
            songs_list.extend([qp(song) for song in songs.split(',')])

        if results.file:
            with open(results.file[0], 'r') as f:
                songs = f.readlines()
                # strip out any empty lines
                songs = filter(None, (song.rstrip() for song in songs))
                # strip out any new lines
                songs = [qp(song.strip()) for song in songs if song]
                songs_list.extend(songs)

        prompt = True if results.has_prompt else False
        quiet = True if results.is_quiet else False
        for song in songs_list:
            query_and_download(song, prompt, quiet)


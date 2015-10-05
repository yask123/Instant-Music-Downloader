#!/usr/bin/env python

from __future__ import print_function
import os
import re

from bs4 import BeautifulSoup

# Version compatiblity
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp


def extract_videos(html):
    """
    Parses given html and returns a list of (Title, Link) for
    every movie found.
    """
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/watch\?v=')
    found = soup.find_all('a', 'yt-uix-tile-link', href=pattern)
    return [(x.text.encode('utf-8'), x.get('href')) for x in found]


def list_movies(movies):
    for idx, (title, _) in enumerate(movies):
        yield '[{}] {}'.format(idx, title)


def search_videos(query):
    """
    Searchs for videos given a query
    """
    response = urlopen('https://www.youtube.com/results?search_query=' + query)
    return extract_videos(response.read())

def query_and_download(search, has_prompts=True, is_quiet=False):
    if not is_quiet:
        print('Searching...')
    
    available = search_videos(search)
    
    if not is_quiet:
        if not available:
            print('No results found matching your query.')
            sys.exit()
        else:
            print('Found:', '\n'.join(list_movies(available)))

    # We only ask the user which one they want if prompts are on, of course
    if has_prompts and not is_quiet:
        choice = ''
        while choice.strip() == '':
            choice = raw_input('Pick one: ')
        title, video_link = available[int(choice)]
        
        prompt = raw_input('Download "%s"? (y/n) ' % title)
        if prompt != 'y':
            sys.exit()
    # Otherwise, just download the first in available list
    else:
        title, video_link = available[0]


    command_tokens = [
        'youtube-dl',
        '--extract-audio',
        '--audio-format mp3',
        '--audio-quality 0',
        'http://www.youtube.com/' + video_link]

    if is_quiet:
        command_tokens.insert(1, '--quiet')

    command = ' '.join(command_tokens)

    # Youtube-dl is a proof that god exists.
    if not is_quiet:
        print('Downloading')
    os.system(command)

    return title

def search_uses_flags(argstring):
    has_flags = False
    if (argstring.find('-p') == 0) or (argstring.find('q') == 0) or (argstring.find('-s') == 0)\
        or (argstring.find('-l') == 0) or (argstring.find('-f') == 0):
        has_flags = True
    return has_flags
                            
def main():
    """
    Run the program session
    """
    argument_string = ' '.join(sys.argv[1:])

    # No command-line arguments
    search = ''

    if not sys.argv[1:]:
        # We do not want to accept empty inputs :)
        while search == '':
            search = raw_input('Enter songname/ lyrics/ artist.. or whatever\n> ')
            search = qp(search)
            query_and_download(search)

    # Deal with 'default' case where -p or -q is specified but not the input type
    # Default is '-s' input type
    elif not argument_string.find('-s') and not argument_string.find('-l') and not argument_string.find('-f'):
        lyrics = ' '.join(argument_string)
        lyrics = lyrics.replace('-p', '').replace('-q', '')
        search = qp(lyrics)

        has_prompt = not argument_string.find('-p')
        is_quiet = argument_string.find('-q')

        downloaded = query_and_download(search, has_prompt, is_quiet)

    # Deal with any cases where no flag is supplied with lyrics, or
    # any number of the input flags are supplied     
    else:
        # No flag
        if not search_uses_flags(argument_string):
           search = qp(' '.join(sys.argv[1:]))
           downloaded = query_and_download(search)
           print("Downloaded %s" % downloaded)


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

            downloads = []
            for song in songs_list:
                downloads.append(query_and_download(song, prompt, quiet))

            print('Downloaded: %s' % ', '.join(downloads))

if __name__ == '__main__':
    main()

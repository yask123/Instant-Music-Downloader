#!/usr/bin/env python
import os
os.system('pip install -r requirements.txt')
current_path = os.getcwd()

os.system('cd ~')
os.system('mkdir .music_downloader')
os.system('cp '+current_path+'/music_downloader.py /.music_downloader')

with open ('.profile','a') as f:
	f.write('PATH="$PATH:~/.music_downloader')

#-*- coding: utf-8 -*-

from io import open as io_open
import sys
import getopt
import requests

CHANNELS_API_URL = 'http://androidapp.1.fm/stlistandroid'
premium = False
out_file = '1FM.m3u'

def parse_cl(argv):

	help_str = sys.argv[0] + ' -p -f <output_filename>'
	try:
		opts, args = getopt.getopt(argv, 'hpf:', ['cl_file='])
	except getopt.GetOptError:
		print(help_str)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(help_str)
			sys.exit()
		elif opt == '-p':
			global premium
			premium = True
		elif opt in ('-f', '--cl_file'):
			global out_file
			out_file = arg
		else:
			sys.exit(2)

def main():

	parse_cl(sys.argv[1:])

	if premium:
		ICECAST_URL = 'http://prmstrm.1.fm:8000/'
	else:
		ICECAST_URL = 'http://strm112.1.fm/'

	print('premium ', premium)
	print('file    ', out_file)

	resp = requests.get(CHANNELS_API_URL)
	channels = resp.json()
	channels_sorted = sorted(channels, key=lambda x: x['StationName'].lower())
	with io_open(out_file, 'w', encoding='utf8') as f:
		f.write("#EXTM3U\n")
		f.write("#PLAYLIST:1.fm\n")
		for channel in channels_sorted:
			station_name = channel['StationName']
			station_desc = channel['StationDesc'].replace('\r\n', '').replace('&amp;', '&').replace('  ', ' ')
			name = f"{station_name} - {station_desc}"
			f.write(f"#EXTINF:-1,{name[:256]}\n")
			f.write(f"{ICECAST_URL}{channel['Stream128k'].split('/')[-1].split('_mobile_mp3')[0]}\n")
	print('channels', len(channels_sorted))

if __name__ == '__main__':
	main()

from io import open as io_open
import requests

ICECAST_URL = 'http://prmstrm.1.fm:8000/'
# ICECAST_URL = 'http://strm112.1.fm/'
CHANNELS_API_URL = 'http://androidapp.1.fm/stlistandroid'


def main():
    resp = requests.get(CHANNELS_API_URL)
    channels = resp.json()
    channels_sorted = sorted(channels, key=lambda x: x['StationName'].lower())
    with io_open('1fm.m3u', 'w', encoding='utf8') as f:
        f.write("#EXTM3U\n")
        f.write("#PLAYLIST:1.fm\n")
        for channel in channels_sorted:
            station_name = channel['StationName']
            station_desc = channel['StationDesc'].replace('\r\n', '').replace('&amp;', '&').replace('  ', ' ')
            name = f"{station_name} - {station_desc}"
            f.write(f"#EXTINF:-1,{name[:256]}\n")
            f.write(f"{ICECAST_URL}{channel['Stream128k'].split('/')[-1].split('_mobile_mp3')[0]}\n")
    print(len(channels_sorted))

if __name__ == '__main__':
    main()
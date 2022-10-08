from pytube import YouTube, Playlist
from tqdm import tqdm
import datetime

playlist_URL = 'https://www.youtube.com/playlist?list=FLNPzWyOogzgJktfz1Uw76hQ'
full_playlist = Playlist(playlist_URL)
output_path = 'music/'


# Fix the video numbers
validation = 'n'
while validation != 'y':
    n = int(input('Enter the number of youtube videos to download: '))
    playlist = full_playlist[:n]
    for URL in playlist:
        vid = YouTube(URL)
        print('Title:', vid.title)
        print('Length:', datetime.timedelta(seconds=vid.length), 's')
        print('URL:', URL)
        print()
    validation = input('Good ? (y/n)')


# Select the correct streams
for URL in tqdm(playlist):
    vid = YouTube(URL)
    audios_dash_mp4 = vid.streams.filter(only_audio=True,
                                         adaptive=True,
                                         file_extension='mp4')

    for i in audios_dash_mp4:
        print(i)
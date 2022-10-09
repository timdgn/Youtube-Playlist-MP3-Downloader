from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
from tqdm import tqdm
import datetime
import os

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


# Select the correct streams (Adaptive/DASH, audio, .mp4)
print("Downloading ...")
for URL in tqdm(playlist):
    vid = YouTube(URL)
    title = vid.title
    audios_dash_mp4 = vid.streams.filter(adaptive=True,
                                         only_audio=True,
                                         file_extension='mp4')
    # Download the stream
    best_audio = audios_dash_mp4[-1]
    best_audio.download(output_path)

print('Download completed !')
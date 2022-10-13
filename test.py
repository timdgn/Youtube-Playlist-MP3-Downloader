import os
import wget
import datetime
from time import sleep
from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
import eyed3
from eyed3.id3.frames import ImageFrame
from rich.progress import track
# import stagger


url = 'https://www.youtube.com/watch?v=6ryAdULXRos&list=FLNPzWyOogzgJktfz1Uw76hQ&index=8'
output_path = 'music'

# Fetch the title of the music
mus = YouTube(url)
title = mus.title
mp4_file = f'.{title}.mp4'
mp3_file = f'{title}.mp3'

# Fetch all the streams available for the music
audios_dash_mp4 = mus.streams.filter(adaptive=True,
                                     only_audio=True,
                                     file_extension='mp4')

# Download a stream to .mp4
best_audio = audios_dash_mp4[-1]  # The last stream has the best quality
print(f'🌟 {title}')
best_audio.download(output_path=output_path,
                    filename=mp4_file,
                    max_retries=3)

print('\n\n\nterminé')
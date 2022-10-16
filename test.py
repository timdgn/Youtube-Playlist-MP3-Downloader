import os
import wget
import datetime
from time import sleep, time
from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
import eyed3
from eyed3.id3.frames import ImageFrame
from rich.progress import track
# import stagger

print('ici 1')
t1 = time()
sleep(1)
t2 = time()

print('ici 2')
time_spent_sec = t2 - t1 + 120
time_spent_min = time_spent_sec / 60

print(f'It took {"%.2f"%time_spent_min} mins !')
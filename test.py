import os
import wget
import datetime
from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
import eyed3
from eyed3.id3.frames import ImageFrame
from rich.progress import track
# import stagger


url = 'https://www.youtube.com/watch?v=6ryAdULXRos&list=FLNPzWyOogzgJktfz1Uw76hQ&index=8'
output_path = 'music'

title = 'hello|world'
if os.name == 'nt':  # On Windows, file names with those characters bring an error
    char_to_replace = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in char_to_replace:
        title = title.replace(char, ' tim ')
print(title)

import os
from os import listdir
from os.path import isfile, join
from time import time
import eyed3
from eyed3.id3.frames import ImageFrame
from rich.progress import track

file_path = 'music'


def tagger(path):
    t1 = time()
    print('\nTagging ...', end='\n\n')

    music_files = [file for file in listdir(path) if isfile(join(path, file))]
    for file in track(music_files, description='[red]Tagging ... '):
        artist = file.split('-')[0]
        artist = artist.strip()

        # Mutagen.eyed3, to tag the artist to the .mp3
        music = eyed3.load(os.path.join(path, file))
        music.tag.artist = artist

        # Save the tag
        music.tag.save(version=eyed3.id3.ID3_V2_3)

    # Compute the time spent on the download part
    t2 = time()
    time_spent_sec = t2 - t1
    time_spent_min = time_spent_sec / 60

    print('\n\n')
    print(f'{len(music_files)} musics tagged in {"%.2f"%time_spent_sec}s ({"%.2f"%time_spent_min}mins) ! ✅')


tagger(file_path)

import os
from os import listdir
from os.path import isfile, join
from time import time
from mutagen.id3 import ID3, TPE1
from mutagen.mp3 import MP3
from rich.progress import track

file_path = 'music'


def tagger(path):
    """
    Tags the artist name to the music metadata, to let music apps group musics by artists.
    :param path: The path where the musics to be tagged are located
    """
    t1 = time()
    print('\nTagging ...', end='\n\n')

    # Selects only the .mp3 files (not directories) in the path
    music_files = [file for file in listdir(path) if isfile(join(path, file)) and '.mp3' in file]
    for file in track(music_files, description='[red]Tagging ... '):

        # Isolates the artist's name
        artist = file.split('-')[0]
        artist = artist.strip()

        # Create some ID3 tags to avoid Mutagen 'ID3NoHeaderError'
        mp3 = MP3(os.path.join(file_path, file))
        if mp3.tags is None:
            mp3.add_tags()
        mp3.save()

        # Loads ID3, tags and saves the tag
        audio = ID3(os.path.join(file_path, file))
        audio['TPE1'] = TPE1(encoding=3, text=artist)
        audio.save()

    # Compute the time spent on the download part
    t2 = time()
    time_spent_sec = t2 - t1
    time_spent_min = time_spent_sec / 60

    print('\n\n')
    print(f'{len(music_files)} musics tagged in {"%.2f"%time_spent_sec}s ! ✅')


if __name__ == '__main__':
    tagger(file_path)

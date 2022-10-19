import os
import datetime
from time import sleep
from pytube import YouTube, Playlist

playlist_URL = 'https://www.youtube.com/playlist?list=FLNPzWyOogzgJktfz1Uw76hQ'
output_path = 'music'


def mus_fetch_reformat(url):
    """
    Takes the url of a YouTube video, and outputs a Pytube object about it.
    It refactors the name of the YouTube video to remove special characters from it
    to avoid file name errors on Windows.
    :param url: URL of a YouTube video
    :return: mus: A Pytube object describing the YouTube video
    """

    mus = YouTube(url)
    # If no sleep, some music names will be presented as "Video Not Available"
    # with a length of 0:05:00s
    sleep(0.5)

    # On Windows, file names with those characters bring an error
    char_to_replace = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in char_to_replace:
        mus.title = mus.title.replace(char, '')

    return mus


def short_playlist(full_pl, output):
    """
    Takes a list of all the URLs of a YouTube playlist,
    and creates a short playlist containing only the musics we want
    :param full_pl: (list) List of URLs of the whole YouTube playlist
    :param output: (str) String of the output path where the musics are to be downloaded
    :return: short_pl: (list) List of URLs of only the selected YouTube videos
    :return: n_music: (int) number of musics we want to download
    """

    global n_music
    validation = 'n'
    short_pl = []
    existing_files = {}

    # While loop to let the user validate if he wants to keep the short playlist shown to him
    while validation not in ['y', 'Y']:
        print('⭐️ 3 different modes:')
        print('1 - Download the x last musics')
        print('2 - Download a range of musics')
        print('3 - Download specific musics')

        dl_mode = 0
        while dl_mode not in [1, 2, 3]:
            dl_mode = int(input('\nWhich mode do you want to use ? (1 or 2 or 3)      '))

        if dl_mode == 1:  # Good !
            n_music = int(input('\nHow many recent musics of your playlist you want to download ?      '))
            print('\n\n')
            short_pl = full_pl[:n_music]

        elif dl_mode == 2:  # Good !
            n_music = input('\nEnter the range of musics to download (e.g. 10-20):      ')
            print('\n\n')
            n_music = n_music.replace(' ', '')
            n_music = n_music.split('-')
            short_pl = full_pl[int(n_music[0])-1:int(n_music[1])-1]

        elif dl_mode == 3:  #
            n_music = input('\nEnter the specific musics you want to download (e.g. 1, 4, 5):      ')
            print('\n\n')
            n_music = n_music.replace(' ', '')
            n_music = n_music.split(',')
            for n in n_music:
                short_pl.append(full_pl[int(n)-1])



        print('Finished !')  # Used to put a break point just after
        print('Breakpoint here !')
        ############################################################################################################




        existing_files = {}

        # Print each music to be downloaded
        for i, URL in enumerate(short_pl):
            mus = mus_fetch_reformat(URL)
            title = mus.title

            print(f'---------- N°{i + 1} ----------')
            print(f'Title: {title}')
            print(f'Length: {datetime.timedelta(seconds=mus.length)}s')
            print(f'URL: {URL}', end='\n\n')

            # If a music already exists, add its name to a list
            if os.path.exists(os.path.join(output, title + '.mp3')):
                existing_files[f'{title}'] = URL

        # Validate if we keep this playlist, of if we want to set a new playlist
        validation = input('Good to download ? (y/n)      ')
        print('\n\n')

    # Remove existing urls from the short_pl list
    [short_pl.remove(URL) for URL in existing_files.values()]

    # Print if there is some musics that were already downloaded
    if len(existing_files) > 0:
        print(f'{len(existing_files)} musics already downloaded over {n_music} in the download list.')
        print('They are not going to be downloaded again :')
        for i, title in enumerate(existing_files.keys()):
            print(f'⭐ {i+1}: {title}')

    return short_pl, n_music


full_playlist = Playlist(playlist_URL)
playlist, n_music = short_playlist(full_playlist, output_path)
print('\n\n\nTerminé')
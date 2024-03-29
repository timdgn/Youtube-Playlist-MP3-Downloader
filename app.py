import os
import wget
import datetime
from time import sleep, time
from rich.progress import track
from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
from mutagen.id3 import ID3, APIC
# https://stackoverflow.com/questions/42473832/embed-album-cover-to-mp3-with-mutagen-in-python-3


def mus_fetch_reformat(url):
    """
    Takes the url of a YouTube video, and outputs a Pytube object about it.
    It refactors the name of the YouTube video to remove special characters from it
    to avoid file name error on Windows
    :param url: URL of a YouTube video
    :return: mus: A Pytube object describing the YouTube video
    """

    mus = YouTube(url)
    while True:
        try:
            _ = mus.title
            break
        except:
            print("Failed to get name. Retrying...")
            sleep(1)
            mus = YouTube(url)
            continue

    sleep(0.5)
    # If no sleep, some music names will be presented as "Video Not Available"
    # with a length of 0:05:00s

    # On Windows, file names with those characters bring an error
    char_to_replace = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in char_to_replace:
        mus.title = mus.title.replace(char, '')

    return mus, mus.title, mus.length


def short_playlist(full_pl, max_length, output):
    """
    Takes a list of all the URLs of a YouTube playlist,
    and creates a short playlist containing only the musics we want
    :param full_pl: (list) List of URLs of the whole YouTube playlist
    :param max_length: maximum length of musics is seconds
    :param output: (str) String of the output path where the musics are to be downloaded
    :return: short_pl: (list) List of URLs of only the selected YouTube videos
    :return: n_music: (int) number of musics we want to download
    """

    global n_music
    short_pl = []
    existing_files = {}
    long_files = {}

    # While loop to let the user validate if he wants to keep the short playlist shown to him
    validation = 'n'
    while validation not in ['y', 'Y']:
        print('⭐️ 3 different modes:')
        print('1 - Download the x last musics')
        print('2 - Download a range of musics')
        print('3 - Download specific musics')
        print('4 - Download the whole playlist (careful with big playlists !)')

        # Option to choose between different download modes
        short_pl = []
        dl_mode = 0
        while dl_mode not in [1, 2, 3, 4]:
            dl_mode = int(input('\nWhich mode do you want to use ? (1 or 2 or 3 or 4)      '))

        if dl_mode == 1:
            n_music = int(input('\nHow many recent musics of your playlist you want to download ?      '))
            print('\n\n')
            short_pl = full_pl[:n_music]

        elif dl_mode == 2:
            n_music = input('\nEnter the range of musics to download (e.g. 10-20):      ')
            print('\n\n')
            n_music = n_music.replace(' ', '')
            n_music = n_music.split('-')
            short_pl = full_pl[int(n_music[0])-1:int(n_music[1])]
            n_music = int(n_music[1]) - int(n_music[0]) + 1

        elif dl_mode == 3:
            n_music = input('\nEnter the specific musics you want to download (e.g. 1, 4, 5):      ')
            print('\n\n')
            n_music = n_music.replace(' ', '')
            n_music = n_music.split(',')
            for n in n_music:
                short_pl.append(full_pl[int(n) - 1])
            n_music = len(n_music)

        elif dl_mode == 4:
            short_pl = full_pl
            n_music = len(full_pl)

        # Print each music to be downloaded
        for i, URL in enumerate(short_pl):
            mus, title, length = mus_fetch_reformat(URL)

            print(f'---------- N°{i + 1} ----------')
            print(f'Title: {title}')
            print(f'Length: {datetime.timedelta(seconds=length)}s')
            print(f'URL: {URL}')

            # If a music already exists in the output path, add its name to a list to avoid downloading it
            if os.path.exists(os.path.join(output, title + '.mp3')):
                existing_files[f'{title}'] = URL

            # If a music length is more than max_length, add its name to a list to avoid downloading it
            if length > max_length and title not in existing_files.keys():
                choice = input(f'⚠ Music longer than {max_length/60} mins, do you want to download it ? ⚠ (y/n)     ')
                if choice not in ['y', 'Y']:
                    long_files[f'{title}'] = URL

            print('\n\n')

        # Validate if we keep this playlist, of if we want to set a new playlist
        validation = input('Good to download ? (y/n)      ')
        print('\n\n')

    # Remove existing urls from the short_pl list
    [short_pl.remove(URL) for URL in existing_files.values()]

    # Remove long files urls from the short_pl list
    [short_pl.remove(URL) for URL in long_files.values()]

    # Print if there is some musics that were already downloaded
    if len(existing_files) > 0:
        print(f'{len(existing_files)} musics already downloaded over {n_music} in the download list.')
        print('They are not going to be downloaded again :')
        for i, title in enumerate(existing_files.keys()):
            print(f'⭐ {i+1}: {title}')

    return short_pl, n_music


def download_pl(short_pl, n_mus, output):
    """
    Select the correct streams (Adaptive/DASH, audio, .mp4) and download the file
    :param short_pl: (list) List of URLs of only the selected YouTube videos
    :param n_mus: (int) number of musics we want to download
    :param output: (str) String of the output path where the musics are to be downloaded
    :return: n_music: (int) number of musics we want to download
    """
    t1 = time()
    print('\nDownloading ...', end='\n\n')

    for i, url in enumerate(track(short_pl, description='[red]Downloading ... ')):
        mus, title, _ = mus_fetch_reformat(url)
        mp4_file = f'.{title}.mp4'
        mp3_file = f'{title}.mp3'

        # Fetch all the streams in Dash/adaptive, audio and .mp4 format
        audios_dash_mp4 = mus.streams.filter(adaptive=True,
                                             only_audio=True,
                                             file_extension='mp4')

        # Download the best stream to .mp4
        best_audio = audios_dash_mp4[-1]  # The last stream has the best quality
        print(f'🌟 {i+1}: {title}')
        best_audio.download(output_path=output,
                            filename=mp4_file,
                            max_retries=3)

        # Convert .mp4 to .mp3 and clean the .mp4
        ff.ffmpeg_extract_audio(os.path.join(output, mp4_file), os.path.join(output, mp3_file))
        os.remove(os.path.join(output, mp4_file))

        # Download the thumbnail
        pic_path_name = wget.download(mus.thumbnail_url, output)

        # mutagen.id3 to tag the thumbnail
        audio = ID3(os.path.join(output, mp3_file))
        with open(pic_path_name, 'rb') as album_art:
            audio['APIC'] = APIC(encoding=3,
                                 mime='image/jpeg',
                                 type=3, desc=u'Cover',
                                 data=album_art.read())
        audio.save()

        # Clean the thumbnail file
        os.remove(pic_path_name)
        print('\n')

    # Compute the time spent on the download part
    t2 = time()
    time_spent_sec = t2 - t1
    time_spent_min = time_spent_sec / 60

    print('\n\n')
    print(f'{n_mus} musics downloaded in {"%.2f"%time_spent_sec}s ({"%.2f"%time_spent_min}mins) ! ✅')


if __name__ == '__main__':
    playlist_URL = 'https://www.youtube.com/playlist?list=FLNPzWyOogzgJktfz1Uw76hQ'
    maximum_length = 900  # 900sec = 15min
    output_path = 'music'

    full_playlist = Playlist(playlist_URL)
    playlist, n_music = short_playlist(full_playlist, maximum_length, output_path)
    download_pl(playlist, n_music, output_path)

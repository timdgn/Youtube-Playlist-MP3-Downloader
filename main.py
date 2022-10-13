import os
import wget
import datetime
from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
import eyed3
from eyed3.id3.frames import ImageFrame
from rich.progress import track
# from tqdm import tqdm
# import stagger


playlist_URL = 'https://www.youtube.com/playlist?list=FLNPzWyOogzgJktfz1Uw76hQ'
output_path = 'music'


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
    existing_files = []

    while validation not in ['y', 'Y']:
        n_music = int(input('\nEnter the number of youtube musics to download: '))
        print('\n\n')
        short_pl = full_pl[:n_music]
        existing_files = []

        # Print each music to be downloaded
        for i, URL in enumerate(short_pl):
            mus = YouTube(URL)
            title = mus.title
            print(f'---------- N°{i + 1} ----------')
            print(f'Title: {title}')
            print(f'Length: {datetime.timedelta(seconds=mus.length)}s')
            print(f'URL: {URL}', end='\n\n')

            # If a music already exists, add its name to a list
            if os.path.exists(os.path.join(output, title + '.mp3')):
                existing_files.append(f'{title}.mp3')

        # Validate if we keep this playlist, of if we want to set a new playlist
        validation = input('Good to download ? (y/n)      ')

    # Print if there is some musics that were already downloaded
    if len(existing_files) > 0:
        print(f'⭐️ {len(existing_files)} musics already downloaded over {n_music} in the download list.')
        print('⭐️ These are not going to be downloaded again :')
        for i, music in enumerate(existing_files):
            print(f'{i+1}: {music}')

    return short_pl, n_music


def download_pl(short_pl, n_mus, output):
    """
    Select the correct streams (Adaptive/DASH, audio, .mp4) and download the file
    :param short_pl: (list) List of URLs of only the selected YouTube videos
    :param n_mus: (int) number of musics we want to download
    :param output: (str) String of the output path where the musics are to be downloaded
    :return: n_music: (int) number of musics we want to download
    """

    print('\n\n')
    print('Downloading ...', end='\n\n')
    bug_list = []
    for i, url in enumerate(track(short_pl, description='Downloading ...')):

        # Fetch the title of the music
        mus = YouTube(url)
        title = mus.title
        mp4_file = f'.{title}.mp4'
        mp3_file = f'{title}.mp3'

        # If the file does not already exist, download it
        if not os.path.exists(os.path.join(output, mp3_file)):  # todo déjà inclu cette fonctionnalité avant

            # Fetch all the streams available for the music
            audios_dash_mp4 = mus.streams.filter(adaptive=True,
                                                 only_audio=True,
                                                 file_extension='mp4')

            # Download a stream to .mp4
            best_audio = audios_dash_mp4[-1]  # The last stream has the best quality
            print(f'\n\n🌟 {i+1}: {title}')
            best_audio.download(output_path=output,
                                filename=mp4_file,
                                max_retries=3)

            # Convert .mp4 to .mp3
            ff.ffmpeg_extract_audio(os.path.join(output, mp4_file), os.path.join(output, mp3_file))
            os.remove(os.path.join(output, mp4_file))

            # Keep track of a failed download
            if not os.path.exists(os.path.join(output, mp3_file)):
                bug_list.append(mp3_file)

            # Download the thumbnail
            pic_path_name = wget.download(mus.thumbnail_url, output)

            # Mutagen.eyed3, to merge the thumbnail to the .mp3
            # https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3
            music = eyed3.load(os.path.join(output, mp3_file))
            if music.tag is None:
                music.initTag()

            # music.tag.title = u'your_title'  # Set the title
            # music.tag.album = u'your_album_name'  # Set the album name
            music.tag.images.set(3,
                                 open(pic_path_name, 'rb').read(),
                                 'image/jpeg')

            # Save the tags
            music.tag.save(version=eyed3.id3.ID3_V2_3)
            music.tag.save()

            # Clean the thumbnail file
            os.remove(os.path.join(pic_path_name))

            # Stagger, it works but the type of the tag is 'Other (0)' instead of 'cover_front (3)',
            # so prefer Mutagen.eyed3
            # https://stackoverflow.com/questions/44480751/how-to-i-obtain-the-album-picture-of-a-music-in-python

            # mp3 = stagger.read_tag(os.path.join(output, mp3_file))
            # print(mp3.artist)  # prints the artist
            # print(mp3.album)  # prints the album
            # print(mp3.picture)  # prints the picture (didn't work with me)
            # print('\n -1- \n')
            #
            # mp3.picture = pic_path_name
            # print(mp3.picture)
            # print('\n -2- \n')
            #
            # mp3.write()
            # print('\n -3- \n')
            #
            # for i in mp3.frames():  # See all the tags
            #     print(i)
            # print('\n -4- \n')

    print('\n\n')
    if n_mus-len(bug_list) == n_mus:
        print('Required music downloaded ! ✅')
    else:
        print(f'Bug detected, downloaded {n_mus-len(bug_list)} musics over {n_mus} ! 🤔')


full_playlist = Playlist(playlist_URL)
playlist, n_music = short_playlist(full_playlist, output_path)
download_pl(playlist, n_music, output_path)

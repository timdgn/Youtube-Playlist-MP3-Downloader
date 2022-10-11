from pytube import YouTube, Playlist
from moviepy.editor import ffmpeg_tools as ff
from tqdm import tqdm
import datetime
import os

playlist_URL = 'https://www.youtube.com/playlist?list=FLNPzWyOogzgJktfz1Uw76hQ'
full_playlist = Playlist(playlist_URL)
output_path = 'music/'

# Set the download playlist
validation = 'n'
while validation not in ['y', 'Y']:
    n_music = int(input('\nEnter the number of youtube musics to download: '))
    print('\n\n\n')
    playlist = full_playlist[:n_music]
    existing_files = []

    # Print each music to be downloaded
    for i, URL in enumerate(playlist):
        mus = YouTube(URL)
        title = mus.title
        print(f'---------- N°{i+1} ----------')
        print(f'Title: {title}')
        print(f'Length: {datetime.timedelta(seconds=mus.length)}s')
        print(f'URL: {URL} \n')

        # If a music already exists, add its name to a list
        if os.path.exists(output_path+title+'.mp3'):
            existing_files.append(f'{title}.mp3')

    # Validate if we keep this playlist, of if we want to set a new playlist
    validation = input('Good to download ? (y/n)      ')
    print('\n\n\n')

# Print if there is some musics that were already downloaded
if len(existing_files) > 0:
    print(f'⭐️ {len(existing_files)} musics already downloaded over {n_music} in the download list.')
    print('⭐️ These are not going to be downloaded again :')
    for i, music in enumerate(existing_files):
        print(f'{i+1}: {music}')

# Select the correct streams (Adaptive/DASH, audio, .mp4)
# and download the file
print('\n\n\n')
print('Downloading ...\n')
bug_list = []
for URL in tqdm(playlist):

    # Fetch the streams
    mus = YouTube(URL)
    title = mus.title
    mp4_file = f'.{title}.mp4'
    mp3_file = f'{title}.mp3'

    # If the file does not already exist, download it
    if not os.path.exists(output_path+mp3_file):
        audios_dash_mp4 = mus.streams.filter(adaptive=True,
                                             only_audio=True,
                                             file_extension='mp4')

        # Download a stream to .mp4
        best_audio = audios_dash_mp4[-1]  # The last stream has the best quality
        best_audio.download(output_path=output_path,
                            filename=mp4_file,
                            max_retries=3)

        # Convert .mp4 to .mp3
        ff.ffmpeg_extract_audio(output_path+mp4_file, output_path+mp3_file)
        os.remove(output_path+mp4_file)

        # Keep track of a failed download
        if not os.path.exists(output_path+mp3_file):
            bug_list.append(mp3_file)


print('\n\n\n')
if n_music-len(bug_list) == n_music:
    print('Required music downloaded ! ✅')
else:
    print('Bug detected \n')
    print(f'Downloaded {n_music-len(bug_list)} musics over {n_music} ! 🤔')

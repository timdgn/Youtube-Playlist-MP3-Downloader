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
while validation != ('y' or 'Y'):
    n = int(input('\nEnter the number of youtube videos to download: '))
    print()
    playlist = full_playlist[:n]
    for URL in playlist:
        vid = YouTube(URL)
        print(f'Title: {vid.title}')
        print(f'Length: {datetime.timedelta(seconds=vid.length)}s')
        print(f'URL: {URL}')
        print()
    validation = input('Good to download ? (y/n)      ')

# Select the correct streams (Adaptive/DASH, audio, .mp4)
print('\nDownloading ...\n')
for URL in tqdm(playlist):

    # Fetch the streams
    vid = YouTube(URL)
    title = vid.title
    audios_dash_mp4 = vid.streams.filter(adaptive=True,
                                         only_audio=True,
                                         file_extension='mp4')

    # Download a stream to .mp4
    best_audio = audios_dash_mp4[-1]
    best_audio.download(output_path=output_path,
                        filename=f'.{title}.mp4',
                                      max_retries=3     )

    # Convert .mp4 to .mp3
    mp4_file = f'.{title}.mp4'
    mp3_file = f'{title}.mp3'
    ff.ffmpeg_extract_audio(output_path+mp4_file, output_path+mp3_file)
    os.remove(output_path+mp4_file)

print('\nDownload completed ! ✅')

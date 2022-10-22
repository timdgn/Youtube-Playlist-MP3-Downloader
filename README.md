# Youtube-Playlist-MP3-Downloader

A simple YouTube music playlist downloader, to always have your favourite music in your pocket when offline 📵

## 1 - How to use ?

1. Install the requirements.txt 📝
2. Run app.py & follow the instructions ✨
3. Run artist_tagger.py ⚡️
4. Listen your music 🎧

## 2 - app.py
### Features

- [x] Give the url of the YouTube playlist, and it outputs .mp3 files.
- [x] The YouTube thumbnail is added to the .mp3 files created.
- [x] Choose between 4 download modes:
  1. Only the x most recent musics of the playlist.
  2. Only a range of musics (e.g. "7-12" to download only the 7th to the 12th music).
  3. Only specific musics (with their rank number in the playlist) (e.g. "7, 12" to download only the 7th and the 12th music).
  4. Setting a whole playlist download (careful with big playlists !).
- [x] Choose to download **or not** musics longer than 15 mins.

### Next features

- [ ] Setting a GUI with PyQT or TK.

## 3 - artist_tagger.py
### Features

- [x] Tags the artist name into the .mp3 metadata
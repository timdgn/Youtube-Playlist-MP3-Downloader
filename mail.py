from pytube import YouTube
# n = int(input("Enter the number of youtube videos to download:"))
# link = input("Enter the link:")
yt = YouTube("https://www.youtube.com/watch?v=Rev25XM9vBE")
#Title of video
print("Title:",yt.title)

#Number of views of video
print("Number of views:",yt.views)

#Length of the video
print("Length of video: ",yt.length,"seconds")
#printing all the available streams
for i in yt.streams:
    print(i)
audios = yt.streams.filter(only_audio=True)
for i in audios:
    print(i)
best_audio = audios.get_highest_resolution()
print("Downloading...")
ys.download('location')
print("Download completed!!")
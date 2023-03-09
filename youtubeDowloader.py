from pytube import YouTube
import urllib.request
import io
import customtkinter
import tkinter
from PIL import ImageTk, Image

class YoutubeDownloader:
    thumbnail_img = None
    video_title = None
    video_resolutions = []
    video_mime_types = []
    videos = []

    def download(choice, videos, path):
            # To validate if the user enters a number displayed on the screen...
            choice = choice + 1
            if 1 <= choice < len(videos):
                # command for downloading the video
                videos[choice - 1].download(path)
                tkinter.messagebox.showinfo(title='Dialog', message='Video was successfully downloaded!')
            else:
                print("Invalid choice!!\n\n")

    def download_test(video_resolutions, videos, path):
        while True:
            # Looping through the video_resolutions list to be displayed on the screen for user selection...
            i = 1
            for resolution in video_resolutions:
                print(f'{i}. {resolution}')
                i += 1

            # To Download the video with the users Choice of resolution
            choice = int(input('\nChoose A Resolution Please: '))

            # To validate if the user enters a number displayed on the screen...
            if 1 <= choice < i:
                resolution_to_download = video_resolutions[choice - 1]
                print(f"You're now downloading the video with resolution {resolution_to_download}...")

                # command for downloading the video
                videos[choice - 1].download(path)

                print("\nVideo was successfully downloaded!")
                break

            else:
                print("Invalid choice!!\n\n")
    def sort_resolutions(url):
        # URL (user input)
        YoutubeDownloader.video_resolutions.clear()
        YoutubeDownloader.video_mime_types.clear()
        YoutubeDownloader.videos.clear()
        my_video = YouTube(url)

        # Title of The Video
        YoutubeDownloader.video_title = my_video.title
        print(my_video.title)

        # Now for the Thumbnail Image
        with urllib.request.urlopen(my_video.thumbnail_url) as u:
            raw_data = u.read()
        dataBytesIO = io.BytesIO(raw_data)
        image = customtkinter.CTkImage(light_image=Image.open(dataBytesIO),
                                       dark_image=Image.open(dataBytesIO),
                                       size=(400, 400))

        YoutubeDownloader.thumbnail_img = image
        print(my_video.thumbnail_url)



        for stream in my_video.streams.filter(type='video').order_by('resolution'):
            # print(stream)
            YoutubeDownloader.video_resolutions.append(stream.resolution)
            YoutubeDownloader.video_mime_types.append(stream.mime_type)
            YoutubeDownloader.videos.append(stream)


        #print(YoutubeDownloader.video_resolutions)
        #print(YoutubeDownloader.video_mime_types)
        #print(YoutubeDownloader.videos)

        return YoutubeDownloader.video_resolutions, YoutubeDownloader.video_mime_types, YoutubeDownloader.videos


#url = input("Please Paste The URL of the youtube video:\n")
# url = "https://youtu.be/o9aaoiyJlcM"

#video_resolutions, videos = sort_resolutions(url)

# download(video_resolutions, videos)


import pytube
import os
from . import gettitle
import moviepy.editor as mp

def mp3(target):
    audio = pytube.YouTube(target.url)
    title = target.title
    output_directory=target.folder
    audio_stream = audio.streams.filter(only_audio=True).first()
    audio_file_path = audio_stream.download(output_path=output_directory, filename="Audio.mp3")
    
def silencer(target):
    video_clip = mp.VideoFileClip(target.video)
    new_video_clip = video_clip.without_audio()
    new_video_clip.write_videofile(f"{target.folder}/xVideo.mp4")

def download_thumbnail(url, output_path):
    try:
        video = YouTube(url)
        thumbnail_url = video.thumbnail_url

        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print('Thumbnail downloaded successfully!')
        else:
            print('Error downloading thumbnail.')
    except Exception as e:
        print(f'Error: {e}')

def mp4(target):
    try:
        video=target.youtube
    except:
        video = pytube.YouTube(target.url)
    title = target.title
    output_directory=target.folder

    # Create a YouTube object and download the video
    video = video.streams.get_highest_resolution()

    print(f'Downloading {title})...')
    video.download(output_path=output_directory, filename="Video.mp4")
    print('Video downloaded successfully!')

    return os.path.join(output_directory,"Video.mp4")

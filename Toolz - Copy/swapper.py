import vlc
from moviepy.editor import AudioFileClip,VideoFileClip
from AudioToolzKit import gettitle

def mp4(target):
    title= target.title

    folder_path=target.folder
    newvideoname="Video_Mix"

    # load the video and audio files
    video = VideoFileClip(f"{folder_path}/Video.mp4")
    new_audio = AudioFileClip(f"{folder_path}/Audio/mix.wav")

    # replace the video's audio with the new audio
    new_video = video.set_audio(new_audio)

    # save the new video file
    new_video.write_videofile(f"{folder_path}/{newvideoname}.mp4")

'''
    title= gettitle.vidname(url)

    folder_path=f"content/{title}"
    newvideoname="Video_vox"

    # load the video and audio files
    video = VideoFileClip(f"{folder_path}/Video.mp4")
    new_audio = AudioFileClip(f"{folder_path}/channels/Audio/vocals.wav")

    # replace the video's audio with the new audio
    new_video = video.set_audio(new_audio)

    # save the new video file
    new_video.write_videofile(f"{folder_path}/{newvideoname}.mp4")

'''

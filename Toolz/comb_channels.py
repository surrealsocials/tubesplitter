import os 
from pydub import AudioSegment
from . import gettitle

def wav(url):
    folder_path=gettitle.vidname(url)

    # Load the 4 separate audio files
    folder_path=f'content/{folder_path}/channels/Audio'
    audio1 = AudioSegment.from_file(os.path.join(folder_path,'bass.wav'), format="wav")
    audio2 = AudioSegment.from_file(os.path.join(folder_path,'other.wav'), format="wav")
    audio3 = AudioSegment.from_file(os.path.join(folder_path,'drums.wav'), format="wav")
    audio4 = AudioSegment.from_file(os.path.join(folder_path,'vocals.wav'), format="wav")

    # Combine the audio files into a single audio segment with 4 channels
    audio_4ch = AudioSegment.empty()
    audio_4ch += audio1.set_channels(2) # set channels to 2 to merge with the next audio file
    audio_4ch += audio2.set_channels(2)
    audio_4ch += audio3.set_channels(2)
    audio_4ch += audio4.set_channels(2)
    name="audio_4ch.wav"
    audio_4ch.export(os.path.join(folder_path,name), format="wav")
    ch4=audio_4ch
    return name

def mp3(url):
    folder_path=gettitle.vidname(url)

    # Load the 4 separate audio files
    folder_path=f'content/{folder_path}/channels/Audio'
    audio1 = AudioSegment.from_file(os.path.join(folder_path,'accompaniment.wav'), format="wav")
    audio2 = AudioSegment.from_file(os.path.join(folder_path,'vocals.wav'), format="wav")

    # Combine the audio files into a single audio segment with 4 channels
    audio_4ch = AudioSegment.empty()
    audio_4ch += audio1.set_channels(1) # set channels to 2 to merge with the next audio file
    audio_4ch += audio2.set_channels(1)

    name="audio_2ch.mp3"
    audio_4ch.export(os.path.join(folder_path,name), format="mp3")

    return name


def stereo(url):
    folder_path=gettitle.vidname(url)

    # Load the separate audio files
    folder_path=f'content/{folder_path}/channels/Audio'

    left_channel = AudioSegment.from_file(os.path.join(folder_path,'accompaniment.wav'))
    right_channel = AudioSegment.from_file(os.path.join(folder_path,'vocals.wav'))

    # Combine the two audio files into a stereo track
    stereo_track = left_channel.overlay(right_channel)

    name="split.wav"
    # Export the stereo track as a new audio file in MP3 format
    stereo_track.export(os.path.join(folder_path,name), format="wav")


from moviepy.editor import AudioFileClip

def create_stereo_track(url):
    folder_path=gettitle.vidname(url)

    # Load the separate audio files
    folder_path=f'content/{folder_path}/channels/Audio'

    # Load the left and right audio files as moviepy audio clips
    left_clip = AudioFileClip(os.path.join(folder_path,'accompaniment.wav'))
    right_clip = AudioFileClip(os.path.join(folder_path,'vocals.wav'))

    # Set the left and right audio clips to the left and right channels, respectively
    left_clip = left_clip.volumex(1.0).audio_pan(1.0, 0.0)
    right_clip = right_clip.volumex(1.0).audio_pan(0.0, 1.0)

    # Combine the left and right audio clips into a single stereo clip
    stereo_clip = left_clip.set_audio(right_clip)

    name="splitstereo.wav"
    # Save the stereo clip to a file
    stereo_clip.write_audiofile(os.path.join(folder_path,name))


def joiner(target):
    folder_path=target.folder
    folder_path=f'{folder_path}/Audio'

    # Load the two audio files
    audio1 = AudioSegment.from_wav(os.path.join(folder_path,'vocals.wav'))
    audio2 = AudioSegment.from_wav(os.path.join(folder_path,'bass.wav'))
    audio3 = AudioSegment.from_wav(os.path.join(folder_path,'other.wav'))
    audio4 = AudioSegment.from_wav(os.path.join(folder_path,'drums.wav'))
    #audio5 = AudioSegment.from_wav(os.path.join(folder_path,'accompaniment.wav'))

    # Set the panning for each audio file (one to the left and one to the right)
    # -1 left, 1 right

    panned_audio1 = audio1.pan(-1)  #
    panned_audio2 = audio2.pan(1)  # 
    panned_audio3 = audio3.pan(1)  # guitar
    panned_audio4 = audio4.pan(-1)  # drums
    panned_audio5 = audio4.pan(1)  # drums


    # Combine the two panned audio files into a single stereo file
    stereo_audio = panned_audio1.overlay(panned_audio2)
    stereo_audio = stereo_audio.overlay(panned_audio4)
    stereo_audio = stereo_audio.overlay(panned_audio5)

    name="mix.wav"
    # Export the stereo audio file to disk as a WAV file
    stereo_audio.export(os.path.join(folder_path,name), format='wav')
    
    '''

    folder_path=gettitle.vidname(url)
    folder_path=f'content/{folder_path}/channels/Audio'

    # Load the two audio files
    audio1 = AudioSegment.from_wav(os.path.join(folder_path,'accompaniment.wav'))
    audio2 = AudioSegment.from_wav(os.path.join(folder_path,'vocals.wav'))

    # Set the panning for each audio file (one to the left and one to the right)
    panned_audio1 = audio1.pan(-1)  # -1 is left channel
    panned_audio2 = audio2.pan(1)  # 1 is right channel

    # Combine the two panned audio files into a single stereo file
    stereo_audio = panned_audio1.overlay(panned_audio2)

    name="newsplit.wav"
    # Export the stereo audio file to disk as a WAV file
    stereo_audio.export(os.path.join(folder_path,name), format='wav')
    '''
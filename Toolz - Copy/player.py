import vlc
import time

def play(target):
    time.sleep(0.2)
    # Create separate VLC media player instances for each file
    vocals = vlc.MediaPlayer()
    guitar = vlc.MediaPlayer()
    drums = vlc.MediaPlayer()
    bass = vlc.MediaPlayer()
    video_player = vlc.MediaPlayer()

    # Load the WAV files and video
    wav1_media = vlc.Media(target.vocals)
    wav2_media = vlc.Media(target.other)
    wav3_media = vlc.Media(target.drums)
    wav4_media = vlc.Media(target.bass)
    video_media = vlc.Media(target.video)
    vocals.set_media(wav1_media)
    guitar.set_media(wav2_media)
    drums.set_media(wav3_media)
    bass.set_media(wav4_media)
    video_player.set_media(video_media)

    # Set the synchronization between the media players
    vocals.set_nsobject(video_player.get_nsobject())
    guitar.set_nsobject(video_player.get_nsobject())
    drums.set_nsobject(video_player.get_nsobject())
    bass.set_nsobject(video_player.get_nsobject())

    # Play the media players
    vocals.play()
    guitar.play()
    drums.play()
    bass.play()
    #video_player.play()

    # Mute the first WAV player when desired
    #video_player.audio_toggle_mute()
    return video_player,vocals,guitar,drums,bass
    # Wait for the playback to finish
    while True:
        state = video_player.get_state()
        if state == vlc.State.Ended:
            break

def stop(target):
    # Cleanup
    target.pvocals.stop()
    target.pguitar.stop()
    target.pdrums.stop()
    target.pbass.stop()
    target.pvideo.stop()

def mute(target,output):
    eval(output).audio_toggle_mute()


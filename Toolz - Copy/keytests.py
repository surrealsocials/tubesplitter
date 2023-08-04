import numpy as np
import matplotlib.pyplot as plt
import IPython.display as ipd
import librosa
import librosa.display
try: from .mykeyfinder import Tonal_Fragment
except: from mykeyfinder import Tonal_Fragment
import soundfile

def getkey(audio_path):
	audio_path = audio_path#'Audio.mp3'
	y, sr = librosa.load(audio_path)
	y_harmonic, y_percussive = librosa.effects.hpss(y)

	mysong = Tonal_Fragment(y_harmonic, sr)
	#mysong.chromagram("Audio")

	mysong = Tonal_Fragment(y_harmonic, sr, tend=22)
	mysong.print_chroma()

	mysong = Tonal_Fragment(y_harmonic, sr, tend=22)
	key = mysong.print_key()
	return key

def movekey():
	steps = float(input("Number of semitones to shift audio file: "))    
	new_y = librosa.effects.pitch_shift(y, sr, steps)
	soundfile.write("pitchShifted.wav", new_y, sr,)

def showbeats(audio_path):
	y, sr = librosa.load(audio_path)
	y_harmonic, y_percussive = librosa.effects.hpss(y)

	# Run the default beat tracker
	tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
	print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

	# Convert the frame indices of beat events into timestamps
	beat_times = librosa.frames_to_time(beat_frames, sr=sr)
	return beat_times

def sync(audio_path1,audio_path2):
	# Beat tracking example
	#audio_path = 'Audio.mp3'
	audio1, samplingrate1 = librosa.load(audio_path1)
	audio2, samplingrte2 = librosa.load(audio_path2)

	length = max(len(audio1), len(audio2))
	audio1 = librosa.util.fix_length(audio1, length)
	audio2 = librosa.util.fix_length(audio2, length)

	max_length = max(len(audio1), len(audio2))
	audio1 = np.reshape(audio1, (max_length,))
	audio2 = np.reshape(audio2, (max_length,))

	y_harmonic, y_percussive = librosa.effects.hpss(audio1)
	y_harmonic, y_percussive = librosa.effects.hpss(audio2)

	# 3. Run the default beat tracker
	tempo1, beat_frames1 = librosa.beat.beat_track(y=audio1, sr=samplingrate1)
	tempo2, beat_frames2 = librosa.beat.beat_track(y=audio2, sr=samplingrte2)

	print('Estimated tempo: {:.2f} beats per minute'.format(tempo1))
	print('Estimated tempo: {:.2f} beats per minute'.format(tempo2))

	# 4. Convert the frame indices of beat events into timestamps
	beat_times1 = librosa.frames_to_time(beat_frames1, sr=samplingrate1)
	beat_times2 = librosa.frames_to_time(beat_frames2, sr=samplingrte2)

	# Compute the beat frames
	frames1 = librosa.beat.beat_track(audio1, samplingrate1, hop_length=512)
	frames2 = librosa.beat.beat_track(audio2, samplingrte2, hop_length=512)

	# Compute the time offsets
	time_offset = beat_times2[0] - beat_times1[0]

	# Synchronize the tracks
	if time_offset > 0:
	    audio1_sync = librosa.effects.time_stretch(audio1, 1.0 + abs(time_offset))
	    audio2_sync = audio2[:len(audio1_sync)]
	    audio2_sync = librosa.effects.time_stretch(audio2_sync, 1.0 / (1.0 + abs(time_offset)))
	else:
	    audio2_sync = librosa.effects.time_stretch(audio2, 1.0 + abs(time_offset))
	    audio1_sync = audio1[:len(audio2_sync)]
	    audio1_sync = librosa.effects.time_stretch(audio1_sync, 1.0 / (1.0 + abs(time_offset)))

	import sounddevice as sd

	# Combine the audio tracks into a single audio array
	combined_audio = audio1_sync + audio2_sync

	# Play the audio
	sd.play(combined_audio, samplingrate1)
	input()

def clicker():
	import librosa
	import numpy as np
	from pydub import AudioSegment

	# Load the audio file
	audio_file = "Audio.mp3"
	audio = AudioSegment.from_file(audio_file)#, format="mp3")
	y, sr = librosa.load(audio_file)

	# Get the beat times
	tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
	beat_times = librosa.frames_to_time(beats, sr=sr)

	# Create a click track with the same tempo as the audio file
	click_duration = int(1000 * len(y) / sr)  # in milliseconds
	click_track = AudioSegment.silent(duration=click_duration)
	click_track = click_track.set_channels(audio.channels)
	click_track = click_track.set_sample_width(audio.sample_width)

	# Add clicks to the click track at the beat times
	click_length = 50  # in milliseconds
	for beat_time in beat_times:
	    click = AudioSegment.silent(duration=click_length)
	    tone = np.sin(2 * np.pi * 1000 * np.arange(int(sr * click_length / 1000)) / sr) * 32767  # generate a 1 kHz tone
	    click = click._spawn(tone.astype(np.int16))
	    click_track = click_track.overlay(click, position=int(1000 * beat_time))

	# Overlay the click track onto the audio file
	output = audio.overlay(click_track)

	# Export the resulting audio file
	output.export("clik.mp3", format="mp3")

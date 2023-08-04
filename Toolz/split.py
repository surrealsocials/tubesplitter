import subprocess,os
import spleeter
from pydub import AudioSegment

def convert_wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

def run(target):
    title = target.title  # Replace with the actual way of getting the title

    # Construct the command arguments
    command_args = [
        "spleeter",
        "separate",
        f"content/{title}/Audio.mp3",
        "-p", "spleeter:4stems",
        "-o", f"content/{title}"
    ]

    if os.path.exists(f"content/{title}/Audio/other.wav") and os.path.exists(f"content/{title}/Audio/drums.wav") and os.path.exists(f"content/{title}/Audio/bass.wav") and os.path.exists(f"content/{title}/Audio/guitar.wav"):
        pass
    else:
        # Run the command using subprocess
        subprocess.run(command_args, shell=True)

    # After running the spleeter separation
    convert_wav_to_mp3(f"content/{title}/Audio/other.wav", f"content/{title}/Audio/other.mp3")
    convert_wav_to_mp3(f"content/{title}/Audio/bass.wav", f"content/{title}/Audio/bass.mp3")
    convert_wav_to_mp3(f"content/{title}/Audio/drums.wav", f"content/{title}/Audio/drums.mp3")
    convert_wav_to_mp3(f"content/{title}/Audio/vocals.wav", f"content/{title}/Audio/vocals.mp3")

    os.remove(f"content/{title}/Audio/other.wav")
    os.remove(f"content/{title}/Audio/bass.wav")
    os.remove(f"content/{title}/Audio/drums.wav")
    os.remove(f"content/{title}/Audio/vocals.wav")



if __name__=="__main__":

    run('target')
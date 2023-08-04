import re,os,json
from . import pytube,vlc
from . import getvideo as gv
from . import split as splitter
from . import comb_channels as comb
from . import swapper as swapvid
from . import player,keytests
import re
class Tube:
	def __init__(self):
		self.resolution="360p"
		self.title=''

	def start(self,url=None,title=None):
		self.url=url
		self.title=title
		self.resolution="360p"
		if not os.path.exists("content"):os.mkdir("content")

	def loadfromurl(self):
		self.resolution="360p"
		self.url=self.url
		self.youtube = pytube.YouTube(self.url)
		self.fulltitle = self.youtube.title
		self.title = self.cleantitle()
		self.folder=f"content/{self.title}"
			
		if not os.path.exists(f'{self.folder}'): os.mkdir(f'{self.folder}')
		if not os.path.exists(f'{self.folder}/Audio'): os.mkdir(f'{self.folder}/Audio')
		self.about=f'{self.folder}/about.json'
		self.save()
			
		
		self.vocals=f"content/{self.title}/Audio/vocals.mp3"
		self.other=f"content/{self.title}/Audio/other.mp3"
		self.drums=f"content/{self.title}/Audio/drums.mp3"
		self.bass=f"content/{self.title}/Audio/bass.mp3"
		self.mix=f"content/{self.title}/Audio/mix.wav"
		self.video=f"content/{self.title}/Video.mp4"
		self.audio=f"content/{self.title}/Audio.mp3"
		self.xvideo=f"content/{self.title}/xVideo.mp4"
		self.video_mix=f"content/{self.title}/Video_Mix.mp4"
		
		#
		
	def loadfromtitle(self):
		print(self.title)
		#url=self.url

		self.folder=f"content/{self.title}"
		if not os.path.exists(f'{self.folder}'):os.mkdir(f'{self.folder}')
		self.about=f'{self.folder}/about.json'
		
		self.vocals=f"{self.folder}/Audio/vocals.mp3"
		self.other=f"{self.folder}/Audio/other.mp3"
		self.drums=f"{self.folder}/Audio/drums.mp3"
		self.bass=f"{self.folder}/Audio/bass.mp3"
		self.mix=f"{self.folder}/Audio/mix.wav"
		self.video=f"{self.folder}/Video.mp4"
		self.audio=f"{self.folder}/Audio.mp3"
		self.xvideo=f"{self.folder}/xVideo.mp4"
		self.video_mix=f"{self.folder}/Video_Mix.mp4"

	def getaudio(self):
		self.loadfromurl()
		gv.mp3(self)

	def getvideo(self):
		print('hi')
		self.loadfromurl()
		print('loaded')
		self.video=gv.mp4(self)
		print("gotvid")

	def fullrun(self):
		self.getvideo()
		self.getaudio()
		self.split()
		self.mixstereo()
		self.swap()

	def save(self):
		jsondata={
			"title":self.title,
			"url":self.url,
			"resolution":self.resolution
		}

		with open(self.about, 'w') as f: 
			f.write(json.dumps(jsondata))

	def cleantitle(self):
		title=self.fulltitle
		
		# Remove all characters except letters, digits, and underscores
		title = re.sub(r'[^\w\s]', '', title)

		# Replace all whitespace with underscores
		title = re.sub(r'\s+', '_', title)

		# Strip any remaining whitespace from the beginning and end of the title
		title = title.strip()[:20]

		return title


	def split(self):
		splitter.run(self)

	def getkey(self):
		self.key=keytests.getkey(self.audio)
		return self.key

	def mixstereo(self):
		comb.joiner(self)

	def swap(self):
		swapvid.mp4(self)

	def stop_video(self):
		self.pvideo.stop()
		self.pguitar.stop()
		self.pvocals.stop()
		self.pbass.stop()
		self.pdrums.stop()


	def play_video(self):
		self.loadfromtitle()

		self.pvideo,self.pvocals,self.pguitar,self.pdrums,self.pbass=player.play(self)

	def togglemute(self,channel):
		if channel == "vocals":
			self.pvocals.audio_toggle_mute()
		elif channel == "guitar":
			self.pguitar.audio_toggle_mute()
		elif channel == "drums":
			self.pdrums.audio_toggle_mute()
		elif channel == "bass":
			self.pbass.audio_toggle_mute()
		elif channel == "video":
			self.pvideo.audio_toggle_mute()







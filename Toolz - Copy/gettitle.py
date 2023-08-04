

def vidname(url):
	youtube = pytube.YouTube(url)
	title = youtube.title[:10].strip().replace(' ','_')

	return title

def fullvidname(url):
	
	youtube = pytube.YouTube(url)
	title = youtube.title

	return title


def clean(url):
	youtube = pytube.YouTube(url)
	filename = youtube.title
	
	# Remove all characters except letters, digits, and underscores
	filename = re.sub(r'[^\w\s]', '', filename)

	# Replace all whitespace with underscores
	filename = re.sub(r'\s+', '_', filename)

	# Strip any remaining whitespace from the beginning and end of the filename
	filename = filename.strip()

	return filename
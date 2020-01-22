from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
import argparse
import json
import os.path
from colorama import init,Fore,Style

# Initialise terminal colors (using colorama)
init(autoreset=True)

# Argument Parser
parser = argparse.ArgumentParser( description="Download MP4 video from a Vimeo Video")
parser.add_argument( "url", type=str, help="The Vimeo URL" )
parser.add_argument( "-q", "--quality", type=str, default="720p", help="Quality level of video (default: 720p)" )
parser.add_argument( "-a", "--all", dest="displayAll", action="store_true", help="Displays all available quality levels")
parser.set_defaults(displayAll=False)
args = parser.parse_args()

# Set variables
quality=args.quality
displayAll=args.displayAll
url=args.url

# Ensure vimeo in URL
if "vimeo" not in url:
	print( "ERROR: \"" + url + "\" is not a valid Vimeo URL" )
	quit()

# Convert to direct video link if required
vimeoPlayerURL="https://player.vimeo.com/video/"
if vimeoPlayerURL not in url:
	sections=url.split('/')
	for section in sections:
		if section.isdigit():
			url=vimeoPlayerURL+section

# Attempt to load the video
try:
	response = requests.get(url)
except ConnectionError:
	print( "ERROR: \"" + url + "\" is not a valid Vimeo URL" )
	quit()


# Function to ensure we do not overwrite any existing files
def GetFileName(title):
	title = re.sub(r'[\\/\:*"<>\|\.%\$\^&£]', '', title) # strip illegal characters from title
	filePath=title+".mp4"

	# Add (#) appropriately if file already exists
	if os.path.exists(filePath):
		for i in range(1,9999):
			filePath=title+" ("+str(i)+").mp4"
			if not os.path.exists(filePath):
				break
	return filePath

# Load the response into BeautifulSoup
soup = BeautifulSoup(response.text, 'lxml')

# ...and parse for the MP4 URLs in the script section
scripts = soup.findAll('script')
for script in scripts:
	config = re.search(r"var config = (.*?);", script.string)
	if config:
		configJson = json.loads(config.group(1))
		title = configJson["video"]["title"]
		print( Style.BRIGHT + "Title: " + Fore.GREEN + title)
		videoSaved=False
		for link in configJson["request"]["files"]["progressive"]:
			if displayAll:
				print("  " + link["quality"])
			elif link["quality"] == quality:
				extractedUrl = link["url"]
				# Sometimes the URL has some redundant characters after the extension
				# This will just remove it
				trim = extractedUrl.rfind(".mp4")
				videoUrl = extractedUrl[:trim] + ".mp4"
				print("  Quality: " + Fore.BLUE + quality)
				print("  Downloading from " + Fore.BLUE + videoUrl)
				fileName=GetFileName(title + " [" + quality + "]")
				print("  Saving to " + Fore.GREEN + fileName)
				video = requests.get(videoUrl)
				with open(fileName, 'wb') as f:
					f.write(video.content)
					videoSaved=True
				break
		if displayAll:
			print("Use " + Fore.GREEN + "-q QUALITY" + Fore.RESET +
					" or " + Fore.GREEN + "--quality QUALITY" + Fore.RESET +
					" to download the quality level required")
		elif not videoSaved:
			print(Fore.RED + "  ERROR: " + Fore.RESET + " Quality level \""+ quality + "\" not available")
			print("Use " + Fore.GREEN + "-a" + Fore.RESET +
					" or " + Fore.GREEN + "--all" + Fore.RESET +
					" to view all available quality levels")

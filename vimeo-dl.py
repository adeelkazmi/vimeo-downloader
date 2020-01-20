# Retrieve the MP4 link from a Vimeo Video
from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
import argparse
import json

# Argument Parser
parser = argparse.ArgumentParser( description="Retrieve MP4 link from a Vimeo Video" )
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

soup = BeautifulSoup(response.text, 'lxml')

# Parse for the MP4 URLs in the script section
scripts = soup.findAll('script')
for script in scripts:
	config = re.search(r"var config = (.*?);", script.string)
	if config:
		links = json.loads(config.group(1))
		for link in links["request"]["files"]["progressive"]:
			if displayAll:
				print(link["quality"])
			elif link["quality"] == quality:
				print(link["url"])


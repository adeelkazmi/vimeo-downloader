# Vimeo Downloader

Download videos from vimeo especially if all you have is a Vimeo Player URL (e.g. https://player.vimeo.com/video/12345678).
This still works with the normal vimeo links as well (https://vimeo.com/12345678).

## Prerequisites

Python3 is required with the requirements detailed in [requirements.txt](requirements.txt)

Download the required python packages using:

    pip install -r requirements.txt

## Usage

To download the mp4 video, by default it will choose 720p:

    python vimeo-dl.py https://player.vimeo.com/video/12345678

To see all the available quality levels:

    python vimeo-dl.py https://player.vimeo.com/video/12345678 --all

And to download the required quality level:

    python vimeo-dl.py https://player.vimeo.com/video/12345678 --quality 1080p

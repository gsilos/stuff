#!/usr/bin/python

# interact with google api youtube

import httplib2
import os
import sys
import re

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                               message="create credentials",
                               scope=YOUTUBE_READONLY_SCOPE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
    flags = argparser.parse_args()
    credentials = run_flow(flow, storage, flags)

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                http=credentials.authorize(httplib2.Http()))

# Retrieve the contentDetails part of the channel resource for the
# authenticated user's channel.


# Retrieve the list of videos uploaded to the authenticated user's channel.
playlistitems_list_request = youtube.playlistItems().list(
    playlistId="PL7DQ_pQCHMdn6NWqcFNTTVhEy3AXE_RJN",
    part="snippet",
    maxResults=50
)

minutos = 0
segundos = 0
contador=0

while playlistitems_list_request:
    playlistitems_list_response = playlistitems_list_request.execute()

    for playlist_item in playlistitems_list_response["items"]:
        video_id = playlist_item["snippet"]["resourceId"]["videoId"]
	print contador,
	print video_id,
        x = youtube.videos().list(part="contentDetails",id=video_id).execute()
        try:
         y = x["items"][0]["contentDetails"]["duration"]
        except IndexError:
	 y = "PT0M0S"
         print "TRETA",
	print y,
	#Ex: PT11M11S
        duration = re.match(r"PT(\d+)M(\d+)?", y)
        m = int(duration.groups('0')[0])
        s = int(duration.groups('0')[1])
	print m, s
	minutos = minutos + m
	segundos = segundos + s
	contador = contador + 1
            
    playlistitems_list_request = youtube.playlistItems().list_next(playlistitems_list_request,
                                                                   playlistitems_list_response)

m, s = divmod(segundos, 60)
h, m = divmod(minutos, 60)
print "Total de tempo da playlist -> %d:%02d:%02d" % (h, m, s)

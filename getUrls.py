from googleapiclient.discovery import build
import os
from urllib.parse import parse_qs, urlparse
import json

youtube = build('youtube', 'v3', developerKey='AIzaSyAgdjsBEBTynMU_u0D66lnb6UeMoqzErko')

def getUrlData(playlist_id):
    urls = {}
    u = 0
    nextPageToken = None
    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails, snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()
        
        for item in pl_response['items']:
            res = {}
            res['videoId'] = item['contentDetails']['videoId']
            res['title'] = item['snippet']['title']
            res['publishedAt'] = item['contentDetails']['videoPublishedAt']
            res['description'] = item['snippet']['description']
            urls[u] = res
            print(u, res['title'])
            u+=1
        
        nextPageToken = pl_response.get('nextPageToken')
        if not nextPageToken:
            break
    return urls

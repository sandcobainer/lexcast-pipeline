"""
Fetch transcripts from each video and load into lex.json
"""

from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
import json 

# Opening JSON file 
f1 = open('urls.json')

# returns JSON object as  
# a dictionary 
d1 = json.load(f1)
for t in d1:
    video_id = d1[t]['videoId']
    try:
        d1[t]['transcript'] = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print('Some error, maybe captions are disabled for', video_id)    

    print('Done: ', t, d1[t]['title'])

with open('lex.json', 'w') as json_file:
  json.dump(d1, json_file)

f1.close()
json_file.close()
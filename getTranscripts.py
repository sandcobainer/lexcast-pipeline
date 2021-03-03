from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
import json 

mongo_client = MongoClient('mongodb://localhost:27017')
host_info = mongo_client['HOST']
print ("host:", host_info)

# lex_collection = database.get_collection("lex")
# # open the weekly_demand json file
# with open("urls.json") as f:
#     file_data = json.load(f)
# # insert the data into the collection
# lex_collection.insert_many(file_data)


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
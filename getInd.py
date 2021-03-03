from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
import json 
import re
import spacy

# Opening JSON file 
f1 = open('lex_ner.json')
lex = json.load(f1)


for i in range(0, len(lex)):
    # create full transcript
    try:
        l = lex[str(i)]['ent']
        lex[str(i)]['ent'] = [dict(s) for s in set(frozenset(d.items()) for d in l)]
    except:
        print('Could not find transcript for: ',i)
    

with open('ner_unique.json', 'w') as json_file:
  json.dump(lex, json_file)
json_file.close()
f1.close()


# lex_collection = database.get_collection("lex")
# # open the weekly_demand json file
# with open("urls.json") as f:
#     file_data = json.load(f)
# # insert the data into the collection
# lex_collection.insert_many(file_data)

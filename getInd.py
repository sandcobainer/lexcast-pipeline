"""
Find unique NER entities and store to JSON file
"""

from youtube_transcript_api import YouTubeTranscriptApi
from pymongo import MongoClient
import json 
import re
import spacy

# Opening JSON file 
f1 = open('lex_ner.json')
lex = json.load(f1)


for i in range(0, len(lex)):
    try:
        l = lex[str(i)]['ent']
        lex[str(i)]['ent'] = [dict(s) for s in set(frozenset(d.items()) for d in l)]
    except:
        print('Error creating unique NER entities ',i)
    

with open('ner_unique.json', 'w') as json_file:
  json.dump(lex, json_file)
json_file.close()
f1.close()
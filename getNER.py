"""
Get Transcripts from Youtube Transcript API and
Perform Named Entity Recognition and Noun Chunking with SpaCy
Link NER entities to transcript timestamp
"""
from youtube_transcript_api import YouTubeTranscriptApi
from collections import Counter
import json 
import time
import spacy
from string import punctuation
from getUrls import getUrlData

nlp = spacy.load("en_core_web_lg")
playlist_id = 'PLrAXtmErZgOdP_8GztsuKi9nrraNbKKp4'
filter_transcript = ['TIME', 'CARDINAL', 'ORDINAL', 'QUANTITY', 'MONEY', 'PERCENT']

def secsToStamps(start):
    return time.strftime('%H:%M:%S', time.gmtime(start))

# get urls, transcripts: EXTRACT
lex = getUrlData(playlist_id)
for t in lex:
    video_id = lex[t]['videoId']
    try:
        lex[t]['transcript'] = YouTubeTranscriptApi.get_transcript(video_id)
    except:
        print('Some error, maybe captions are disabled for', video_id)    
    print('Done: ', t, lex[t]['title'])

# get NER, concepts: TRANSFORM
for t in lex:
    try:
        transcript = lex[t]['transcript']

        # create full transcript
        full_transcript = ''
        for chunk in lex[t]['transcript']:
            full_transcript += ' ' + chunk['text']
            
        print('full transcript created: ', lex[t]['videoId'])
        # run ner
        nlp_transcript = nlp(full_transcript)
        lex[t]['ents'] = []
        lex[t]['nouns'] = []
        pos_tag = ['PROPN','NOUN','ADJ']
        
        # get some important words from noun chunks
        # use these for keywords and bag of words modelling
        for chunk in nlp_transcript.noun_chunks:
            final_chunk = ""
            for token in chunk:
                if (token.pos_ in pos_tag):
                    final_chunk =  final_chunk + token.text + " "
            if final_chunk:
                lex[t]['nouns'].append(final_chunk.strip())
                        
        # store ner events with timestamps
        for ent in nlp_transcript.ents:
            if (ent.label_ not in filter_transcript):
                for chunk in lex[t]['transcript']:
                    if ent.text in chunk['text']:
                        if ent.label_ == 'DATE':
                            if ent.text.isdigit():
                                lex[t]['ents'].append({
                                    ent.text:ent.label_,
                                    'timestamp':secsToStamps(chunk['start'])
                                })
                        else:
                            lex[t]['ents'].append({
                                    ent.text:ent.label_,
                                    'timestamp':secsToStamps(chunk['start'])
                                })

        lex[t].pop('transcript')
        # lex[t].pop('description')

    except Exception as e:
        print(e)


# write data for each episode to big output json file : LOAD
# can be used as our over-arching database apart from urls.json
with open('lex_ner.json', 'w') as json_file:
  json.dump(lex, json_file)
json_file.close()




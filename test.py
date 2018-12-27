from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from apiclient.http import MediaIoBaseDownload
import Vokaturi

from flask import Flask
from flask import request
from flask import make_response

import os
import json
app = Flask(__name__)

Vokaturi.load("lib/open/linux/OpenVokaturi-3-0-linux64.so")
SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def hello():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    file_id='1O9mlQFlJ5dTRZvc9SFwj2FBn3KCyN32k'
    request = service.files().get_media(fileId=file_id)
    
#    fh = io.FileIO('test.wav','wb')
#    downloader = MediaIoBaseDownload(fh, request)
#    done = False
#    while done is False:
#        status, done = downloader.next_chunk()
#        print ("Download %d%%." % int(status.progress() * 100))
    
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%." % int(status.progress() * 100))
    print(fh.getbuffer().nbytes)
    buffer_length = fh.getbuffer().nbytes
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    c_buffer[:] = fh.getvalue() 
    voice = Vokaturi.Voice (8000, buffer_length)
    voice.fill(buffer_length, c_buffer)
    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)
    
    output = ""
    
    if quality.valid:
        output += emotionProbabilities.neutrality
        output += emotionProbabilities.happiness
        output += emotionProbabilities.sadness
        output += emotionProbabilities.anger
        output += emotionProbabilities.fear
    else:
        output += "Not enough sonorancy to determine emotions"
    
    return output

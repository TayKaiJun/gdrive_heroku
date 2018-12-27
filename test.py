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

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    
    #Obtain info from the query in Dialogflow
    result = req.get("queryResult")
    parameters = result.get("parameters")
    
    fileName = parameters.get("FolderType")
    
    #verify credentials to use google drive API
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    #hardcoded a file ID of the 'hello.wav' file on google drive
    file_id='1O9mlQFlJ5dTRZvc9SFwj2FBn3KCyN32k'
    request = service.files().get_media(fileId=file_id)
    
    #downloads binary data of wav file and stored in a buffered stream
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        #print ("Download %d%%." % int(status.progress() * 100))
    #print(fh.getbuffer().nbytes)
    
    #parse buffered stream into Vokaturi (TO-DO: FIX BYTE CONVERSION)
    buffer_length = fh.getbuffer().nbytes
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    c_buffer[:] = fh.getvalue() 
    voice = Vokaturi.Voice (8000, buffer_length)
    voice.fill(buffer_length, c_buffer)
    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)
    
    #Output data from Vokaturi
    output = "The results of the analysis of " + fileName " is... "
    
    if quality.valid:
        output += 'Neutral: %.5f, ' % emotionProbabilities.neutrality
        output += 'Happiness: %.5f, ' % emotionProbabilities.happiness
        output += 'Sadness: %.5f, ' % emotionProbabilities.sadness
        output += 'Anger: %.5f, ' % emotionProbabilities.anger
        output += 'Fear: %.5f' % emotionProbabilities.fear
    else:
        output += "Not enough sonorancy to determine emotions"
    
    return {
        "fulfillmentText": output
    }

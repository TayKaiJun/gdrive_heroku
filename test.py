from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import io
from apiclient.http import MediaIoBaseDownload

from flask import Flask
from flask import request
from flask import make_response

import os
import json
app = Flask(__name__)
SCOPES = 'https://www.googleapis.com/auth/drive'

@app.route('/')
def hello():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    output = ""
    
    if not items:
        output += 'No files found.'
    else:
        output += 'Files:'
        for item in items:
            output += u'{0} ({1})'.format(item['name'], item['id'])
            output += '\n'
    
    return output
        

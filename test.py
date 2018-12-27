import os
import json

from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World'
    
        

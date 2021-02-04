from flask import Flask
from flask import request
from . import Twinsie

app = Flask(__name__)

@app.route('/')
def run():
    return f'Welcome to Twinsie where two strings of text are compared and given a score between 0 and 1. \
    <br><br> \
    Send a POST request with text1 and text2 to our twinsie endpoint to compare the two strings of text.'

@app.route('/twinsie', methods=['POST'])
def twinsie():
    req = request.get_json()
    str1 = req['text1']
    str2 = req['text2']
    task = Twinsie(str1, str2)
    return task.run()

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World '

"""
アプリの立ち上げ方
set FLASK_APP = ***.py
flask run
Running on htttp://127.0.0.1:5000
"""

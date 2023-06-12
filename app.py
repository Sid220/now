from flask import Flask, render_template
import json
import random
import db
import vid_manager
from flask import request

app = Flask(__name__)


@app.route('/api/get_vids')
def get_vids():
    return vid_manager.get_rand_vids()


@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/api/download_vids')
def download_vids():
    return vid_manager.download_vids(request)


if __name__ == '__main__':
    app.run()

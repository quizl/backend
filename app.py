import os
import requests
from flask import Flask, render_template, request
from quizler.utils import get_user_sets

app = Flask(__name__)

client_id = os.environ.get('CLIENT_ID')
secret_key = os.environ.get('SECRET_KEY')

@app.route("/")
def root():
    code = request.args.get('code')
    state = request.args.get('state')
    if code and state:
        url = 'https://api.quizlet.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'http://localhost:5000/',
        }
        auth = requests.auth.HTTPBasicAuth(client_id, secret_key)
        response = requests.post(url, data=data, auth=auth)
        if response.status_code == 200:
            user_sets = get_user_sets(client_id, response.json()['user_id'])
            return render_template('sets.html', sets=user_sets)
    return render_template('start.html', client_id=client_id)

import os
import requests
from flask import Flask, render_template, request, session
from quizler.utils import get_user_sets, reset_term_stats

app = Flask(__name__)

app.secret_key = os.environ.get('HTTP_SESSION_SECRET_KEY')
client_id = os.environ.get('QUIZLET_CLIENT_ID')
secret_key = os.environ.get('QUIZLET_SECRET_KEY')

@app.route('/')
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
            session['user_id'] = response.json()['user_id']

    if 'user_id' in session:
        user_id = session['user_id']
        user_sets = get_user_sets(client_id, user_id)
        return render_template('sets.html', sets=user_sets)

    return render_template('start.html', client_id=client_id)

@app.route('/api/1.0/reset/<setname>/<term>', methods=['PUT'])
def reset(setname, term):
    reset_term_stats(setname, term, client_id, session['user_id'])

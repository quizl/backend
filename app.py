import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('start.html', client_id=os.environ.get('CLIENT_ID'))

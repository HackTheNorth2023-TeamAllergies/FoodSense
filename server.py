from flask import Flask, redirect, url_for, session, render_template
from flask_oauthlib.client import OAuth
import requests  
import os
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from werkzeug.utils import redirect
from Backend.Models.userActions import Database 
from os import environ
from Backend.Models.models import User 

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='272504189571-40ofg7aofv8grvjpiho5eqlegor7gqep.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email',  # Add more scopes as needed
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)
database = Database("cockroachdb://ethan:lO1JVTfkDQwKwtEelSo6gA@zippy-seeker-5493.g8z.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))
    

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('google_email', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    
    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    session['google_email'] = user_info.data['email']
    newUser = database.create_user(user_info.data['email'], " ", " ", " ")
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')



if (__name__ == '__main__'):
    app.run(debug = True)


#DB_URI = "cockroachdb://rahul:bKlrahcb9ICUCT6z-vlFig@free-tier.us-east1.cockroachlabs.cloud:26257/game?sslmode=require&options=--cluster%3Dpink-lioness-5406"

#cat dbinit.sql | cockroach sql --url "postgresql://ethan:lO1JVTfkDQwKwtEelSo6gA@zippy-seeker-5493.g8z.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"

#

# coding: utf-8
# app.py

from flask import Flask, request, make_response, jsonify,render_template
import os
import werkzeug
import flask_login
from datetime import datetime
import imp
import common as cmn
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import staticlogic as sl

CSVSAVE_DIR = '.\\csvdata\\'
IMGSAVE_DIR = '.\\plotimgtmp\\'

app = Flask(__name__)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'foo@bar.tld': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/linearregression',methods=['POST'])
def upload_multipart():
  #csv upload logic
  if 'uploadFile' not in request.files:
    make_response(jsonify({'result':'uploadFile is required.'}))
  
  file = request.files['uploadFile']
  #fileName = file.filename
  if '' == file.filename:
    make_response(jsonify({'result':'filename must not empty.'}))
  
  saveFileName = file.filename
  file.save(os.path.join(CSVSAVE_DIR, saveFileName))
  result,image = sl.stserveLinearRegression(saveFileName,IMGSAVE_DIR + 'lr.png')
  return render_template('linearregression.html',image=image)

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
  print("werkzeug.exceptions.RequestEntityTooLarge")
  return 'result : file size is overed.'

if __name__ == '__main__':
    app.debug = True
    #print(app.url_map)
    app.run(host='0.0.0.0', port=10080)
# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, flash, render_template, request, redirect, url_for
app = Flask

import os
from flask_sqlalchemy import SQLAlchemy
from flask import session

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
with app.app_context():
    db.create_all()

@app.route('/', methods = ['GET'])
def index():

    username = None
    if 'user_id' in session:
        user = Users.query.get(session['user_id'])
        if user:
            username = user.username
            
    return render_template('index.html', user_name = username)

@app.route('/api/login', methods =['POST'])
def login():
    if request.method == 'POST':

        id = request.form['id']
        password = request.form['password']

        user = Users.query.filter_by(userid=id, password=password).first()

        if user:

            session['user_id'] = user.userid
            flash('로그인 성공', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 아이디 또는 비밀번호가 올바르지 않습니다.')

    return render_template('index.html')        
    
if __name__ == '__main__':
    app.run(debug=True) 
# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session

app = Flask(__name__)

import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/membership', methods=['GET', 'POST'])
def membership():
    if request.method == 'POST':
        userid = request.form['id']
        username = request.form['username']
        password = request.form['password']

        # 비밀번호 해시화
        hashed_password = generate_password_hash(password, method='sha256')

        # 새로운 사용자 생성
        new_user = Users(userid=userid, username=username, password=hashed_password)

        # 데이터베이스에 추가
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공. 로그인하세요!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

app = Flask(__name__, static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db = SQLAlchemy(app)

class Users(db.Model):
    userid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

# 캐시 없음 헤더 설정
@app.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/membership', methods=['POST'])
def membership():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']

        # 사용자가 이미 존재하는지 확인
        if Users.query.filter_by(userid=id).first():
            flash('이미 존재하는 아이디입니다.', 'error')
            return redirect(url_for('sign'))

        # 새로운 사용자 생성
        new_user = Users(userid=id, username=username, password=generate_password_hash(password, method='sha256'))

        # 새 사용자를 데이터베이스에 추가
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공! 로그인해주세요.', 'success')
        return redirect(url_for('sign'))

    return render_template('sign.html')  # 기존의 회원가입 페이지로 이동


if __name__ == '__main__':
    app.run(debug=True)
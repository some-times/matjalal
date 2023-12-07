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

@app.route('/api/member', methods=['POST'])
def member():
    if request.method == 'POST':
        id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        # 서버 측 유효성 검사
        if not id or not username or not password or not password_confirmation:
            flash('모든 필드를 채워주세요.', 'error')
            return redirect(url_for('sign'))

        if password != password_confirmation:
            flash('비밀번호와 비밀번호 확인이 일치하지 않습니다.', 'error')
            return redirect(url_for('sign'))

        if Users.query.filter_by(userid=id).first():
            flash('이미 존재하는 아이디입니다.', 'error')
            return redirect(url_for('sign'))

        # 비밀번호를 해시하여 데이터베이스에 저장
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = Users(userid=id, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공! 로그인해주세요.', 'success')
        return redirect(url_for('sign'))

    return render_template('sign.html')


if __name__ == '__main__':
    app.run(debug=True)
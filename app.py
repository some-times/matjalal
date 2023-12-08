# 필수 라이브러리
'''
0. Flask : 웹서버를 시작할 수 있는 기능. app이라는 이름으로 플라스크를 시작한다
1. render_template : html파일을 가져와서 보여준다
'''
from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db = SQLAlchemy(app)


class Users(db.Model):
    userid = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Restarants(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    shopname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    style = db.Column(db.String(20), nullable=False)
    review = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(1000), nullable=False)


with app.app_context():
    db.create_all()


@app.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/search', methods=['GET'])  # 검색
def search():
    if 'user_id' in session:      
        username = None
        if 'user_id' in session:
            user = Users.query.get(session['user_id'])
            if user:
                username = user.username

    query = request.args.get('query')
    restarant_list = Restarants.query.filter(Restarants.shopname.like(f'%{query}%') |
                                                Restarants.style.like(f'%{query}%')).all()

    return render_template('main.html', restarant_list = restarant_list, user_name = username)

@app.route('/restarant.html', methods=['POST', 'GET']) # 식당 추가 페이지 이동
def foodie_move():
    if 'user_id' in session:      
        username = None
        if 'user_id' in session:
            user = Users.query.get(session['user_id'])
            if user:
                username = user.username
        return render_template('restarant-1.html', user_name = username)

    alert_msg = "로그인이 필요합니다."

    return render_template('sign.html', msg = alert_msg)
            
#파일명을 겹치지 않기 위한 함수
def generate_unique_filename(filename):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
    _, extension = os.path.splitext(filename)
    unique_filename = timestamp + extension
    return unique_filename

# 식당 추가


@app.route('/api/foodie', methods=['POST'])
def foodie_create():

    try: 
        userid_receive = session['user_id']
        username_receive = session['user_name']
        shopname_receive = request.form['shopname']
        address_receive = request.form['address']
        style_receive = request.form['style']
        review_receive = request.form['review']
        uploaded_file = request.files['img']
        filename = uploaded_file.filename
        unique_filename = generate_unique_filename(filename)
        uploaded_file.save("./static/upload/"+unique_filename+".jpeg")
    except SQLAlchemyError as e:
        flash("오류가 발생했습니다.")


    restarant = Restarants(userid = userid_receive, username = username_receive, shopname = shopname_receive, 
                            address =  address_receive, style  = style_receive, review = review_receive, img = unique_filename)
    db.session.add(restarant)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/api/foodie/', methods=['POST'])
def foodie_delete():
    id_receive = request.form['id']
    user_id = session['user_id']
    try:
        delete_restarant = Restarants.query.filter_by(userid = user_id, id = id_receive).first() 
        db.session.delete(delete_restarant)
        db.session.commit()
        flash("삭제되었습니다 .")

    except SQLAlchemyError as e:
        flash("권한이 없습니다.")

    return redirect(url_for('index'))

# 회원가입/로그인 페이지
@app.route('/sign.html', methods=['GET', 'POST'])
def sign():
    return render_template('sign.html')

# 로그인페이지에서 메인으로 돌아가기
@app.route('/main.html', methods=['GET', 'POST'])
def index_back():
    return render_template('main.html')

# 메인 페이지
@app.route('/', methods=['GET'])
def index():
    username = None
    if 'user_id' in session:
        user = Users.query.get(session['user_id'])
        if user:
            username = user.username
            
    restarant_list = Restarants.query.all()

    return render_template('main.html', user_name = username, restarant_list = restarant_list)

# 로그인
@app.route('/api/login', methods=['POST'])
def login():
    if request.method == 'POST':
        id = request.form['id']
        password = request.form['password']
        user = Users.query.filter_by(userid=id).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.userid
            session['user_name'] = user.username
            session.permanent = True
            flash('로그인 성공', 'success')
            return redirect(url_for('index'))
        else:
            flash('로그인 실패. 아이디 또는 비밀번호가 올바르지 않습니다.')

    return render_template('main.html')

# 세션 체크
@app.route('/api/check_login_status', methods=['GET'])
def check_login_status():
    if 'user_id' in session:
        return jsonify({'isLoggedIn': True, 'userId': session['user_id']})
    else:
        return jsonify({'isLoggedIn': False})
    
# 로그아웃
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return jsonify({'message': 'success'})

# 캐시 없음 헤더 설정
@app.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# 회원가입
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
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')
        new_user = Users(userid=id, username=username,
                        password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공! 로그인해주세요.', 'success')
        return redirect(url_for('index'))

    return render_template('index')


# 회원가입 아이디 유효성 검사
@app.route('/api/check_duplicate', methods=['POST'])
def check_duplicate_id():
    data = request.get_json()
    user_id = data.get('userId', '')

    exist_user = Users.query.filter_by(userid=user_id).first()

    if exist_user:
        return jsonify({'isDuplicate': True})
    else:
        return jsonify({'isDuplicate': False})

# 로그인 비밀번호 유효성 검사
@app.route('/api/check_password', methods=['POST'])
def check_password():
    id = request.form.get('id')
    password = request.form.get('password')
    user = Users.query.filter_by(userid = id).first()

    if user and check_password_hash(user.password, password):
        return jsonify({'isValid': True})
    else:
        return jsonify({'isValid': False}) 


# 상세페이지 이동
@app.route('/restarant/<int:restarant_id>', methods=['GET'])
def restarant_detail(restarant_id):
    # restarant_id에 해당하는 레스토랑 정보를 데이터베이스에서 가져와서 상세 페이지에 전달
    restarant = Restarants.query.get_or_404(restarant_id)
    username = None
    userid = None
    if 'user_id' in session:      
        if 'user_id' in session:
            user = Users.query.get(session['user_id'])
            if user:
                userid = user.userid
                username = user.username
    return render_template('restarant_detail.html', restarant=restarant, user_name = username, user_id = userid)

if __name__ == '__main__':
    app.run(debug=True)
s
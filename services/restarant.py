from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config["SECRET_KEY"] = "ABCD"

db = SQLAlchemy(app)

class Restarants(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    shopname = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    style = db.Column(db.String(20), nullable=False)
    review = db.Column(db.String(500), nullable=False)
    img = db.Column(db.String(1000), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/') # main, 모든 리스트 출력
def index():
    restarant_list = Restarants.query.all()

    return render_template('main.html', restaurant_list = restarant_list)

@app.route('/search', methods=['GET']) # 검색
def search():
    query = request.args.get('query')
    restarant_list = Restarants.query.filter(Restarants.shopname.like(f'%{query}%') |
                                                Restarants.style.like(f'%{query}%')).all()

    return render_template('main.html', restarant_list = restarant_list)

@app.route('/restarant.html', methods=['POST', 'GET']) # 식당 추가 페이지 이동
def foodie_move():
    return render_template('restarant-1.html')

@app.route('/api/foodie', methods=['POST']) #식당 추가
def foodie_create():
    try: 
        userid_receive = request.form['userid']
        username_receive = request.form['username']
        shopname_receive = request.form['shopname']
        address_receive = request.form['address']
        style_receive = request.form['style']
        review_receive = request.form['review']
        uploaded_file = request.files['img']
        img_name = uploaded_file.filename
        uploaded_file.save("./static/upload/"+img_name+".jpeg")
    except SQLAlchemyError as e:
        flash("오류가 발생했습니다.")

    restarant = Restarants(userid = userid_receive, username = username_receive, shopname = shopname_receive, 
                            address =  address_receive, style  = style_receive, review = review_receive, img = img_name)
    db.session.add(restarant)
    db.session.commit()
    
    return redirect(url_for('index'))
    #return redirect(url_for('index.html'))

@app.route('/api/foodie/', methods=['POST']) 
#@app.route('/api/foodie/<id>', methods=['post']) 삭제
def foodie_delete():
    #userid = session['userid']
    id = 1
    userid = 'test'

    try:
        delete_restarant = Restarants.query.filter_by(userid = userid, id = id).first() 
        db.session.delete(delete_restarant)
        db.session.commit()
        flash("삭제되었습니다 .")

    except SQLAlchemyError as e:
        flash("권한이 없습니다.")

    return render_template('restarant.html')


if __name__ == '__main__':
    app.run()
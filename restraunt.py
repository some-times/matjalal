from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Restaurants(db.Model):
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

@app.route('/')
def index():
    restaurant_list = Restaurants.query.all()

    return render_template('index.html', restaurant_list = restaurant_list)

@app.route('/api/foodie', methods=['POST'])
def foodie_create():
    userid_receive = request.args.get("userid")
    username_receive = request.args.get("username")
    shopname_receive = request.args.get("shopname")
    address_receive = request.args.get("address")
    style_receive = request.args.get("style")
    review_receive = request.args.get("review")
    img_receive = request.args.get("img")

    print(userid_receive, username_receive, shopname_receive, address_receive,
            style_receive, review_receive, img_receive)
    # restaurant = Restaurants(userid = userid_receive, username = username_receive, shopname = shopname_receive, 
    #                         address =  address_receive, style  = style_receive, review = review_receive, img = img_receive)
    # db.session.add(restaurant)
    # db.session.commit()
    return render_template('index.html')

    #return redirect(url_for('index.html'))

@app.route('/api/foodie', methods=['DELETE'])
def foodie_delete():
    userid_receive = request.args.get("userid")
    id_receive = request.args.get("id")

    delete_restraurant = Restaurants.query.filter_by(userid = userid_receive, id = id_receive).first()
    db.session.delete(delete_restraurant)
    db.session.commit()

    return redirect(url_for('index.html'))

# @app.route('/foodie/<query>')
# def search(query):
#     restaurant_list = Restaurants.query.filter_by((shopname = query) | (style = query)).all()

#     return render_template('index.html', restaurant_list = restaurant_list)

if __name__ == '__main__':
    app.run()
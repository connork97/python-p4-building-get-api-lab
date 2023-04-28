#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = []

    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        all_bakeries.append(bakery_dict)
    
    response = make_response(jsonify(all_bakeries), 200)

    print(response)
    return response

    # bakeries = Bakery.query.all()
    # bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    # response = make_response(
    #     jsonify(bakeries_serialized),
    #     200
    # )
    # response.headers['Content-Type'] = 'application/json'
    # return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    found_bakery = Bakery.query.filter(Bakery.id == id).first()
    found_bakery_dict = found_bakery.to_dict()
    response = make_response(found_bakery_dict, 200)
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_price_serialized = []

    for baked_good in baked_price:
        baked_good_dict = baked_good.to_dict()
        baked_price_serialized.append(baked_good_dict)

    response = make_response(jsonify(baked_price_serialized), 200)

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    most_expensive_dict = most_expensive.to_dict()

    response = make_response(jsonify(most_expensive_dict), 200)

    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)

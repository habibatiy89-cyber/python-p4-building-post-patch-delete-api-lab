#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return "Welcome to the Bakery API"

# GET all bakeries
@app.route('/bakeries')
def bakeries():
    return make_response([b.to_dict() for b in Bakery.query.all()], 200)

# GET bakery by id / PATCH bakery name
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        return make_response({"message": "Bakery not found."}, 404)

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        if 'name' in request.form:
            bakery.name = request.form.get('name')
        db.session.add(bakery)
        db.session.commit()
        return make_response(bakery.to_dict(), 200)

# GET all baked goods / POST new baked good
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        return make_response([bg.to_dict() for bg in BakedGood.query.all()], 200)

    elif request.method == 'POST':
        new_bg = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )
        db.session.add(new_bg)
        db.session.commit()
        return make_response(new_bg.to_dict(), 201)

# GET baked good by id / DELETE baked good
@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_good_by_id(id):
    bg = BakedGood.query.get(id)
    if not bg:
        return make_response({"message": "Baked good not found."}, 404)

    if request.method == 'GET':
        return make_response(bg.to_dict(), 200)

    elif request.method == 'DELETE':
        db.session.delete(bg)
        db.session.commit()
        return make_response({"delete_successful": True, "message": "Baked good deleted."}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)

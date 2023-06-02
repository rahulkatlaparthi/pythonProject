import json
from json import JSONEncoder

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# New

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationship.db'
# app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///two.db'}

# Init database
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Create class and Model Marshmallow Schema


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, name, password):
        self.name = name
        self.password = password


class DrinkSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'password')


drink_schema = DrinkSchema()
drinks_schema = DrinkSchema(many=True)


class Result:
    success = False

    def __init__(self, success):
        self.success = success


class ResultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


# class ResultSchema(ma.Schema):
#     class Meta:
#         fields = ('success')
#
#
# result_schema = ResultSchema()


# class Veg(db.Model):
#     __bind_key__ = 'two'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     image = db.Column(db.String(200))
#     qty = db.Column(db.Integer)
#     price = db.Column(db.Float)
#
#     def __init__(self, name, image, qty, price):
#         self.name = name
#         self.image = image
#         self.qty = qty
#         self.price = price

#
# class VegSchema(ma.Schema):
#     class Meta:
#         fields = ('id', 'name', 'image', 'qty', 'price')
#
#
# veg_schema = VegSchema()
# veg_schema = VegSchema(many=True)

# Route settings
# create a drink
@app.route('/drink', methods=['POST'])
def add_drink():
    name = request.json['name']
    password = request.json['password']

    new_drink = Drink(name, password)
    db.session.add(new_drink)
    db.session.commit()
    return drink_schema.jsonify(new_drink)


# Get all drinks
@app.route('/drink', methods=['GET'])
def get_drinks():
    all_drinks = Drink.query.all()
    result = drinks_schema.dump(all_drinks)
    return jsonify(result)


# Get single drink
@app.route('/drink/<id>', methods=['GET'])
def get_drink(id):
    drink = Drink.query.get(id)
    return drink_schema.jsonify(drink)


# Update a drink
@app.route('/drink/<id>', methods=['PUT'])
def update_drink(id):
    drink = Drink.query.get(id)

    name = request.json['name']
    image = request.json['image']
    qty = request.json['qty']
    price = request.json['price']

    drink.name = name
    drink.image = image
    drink.qty = qty
    drink.price = price

    db.session.commit()
    return drink_schema.jsonify(drink)


# Validate a drink
@app.route('/validatedrink', methods=['POST'])
def validate_drink():
    name = request.json['name']
    password = request.json['password']
    drink = Drink.query.filter_by(name=name, password=password)
    items = drinks_schema.dump(drink)
    print(items)
    result = Result(success=False)
    print(result.success)
    if len(items) == 0:
        result.success = False

    else:
        result.success = True

    return json.dumps(ResultEncoder().encode(result))


# Delete single drink
@app.route('/drink/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    return drink_schema.jsonify(drink)


# @app.route('/veg', methods=['GET'])
# def get_veg():
#     all_drinks = Veg.query.all()
#     result = veg_schema.dump(all_drinks)
#     return jsonify(result)
#
#
# @app.route('/veg', methods=['POST'])
# def add_veg():
#     name = request.json['name']
#     image = request.json['image']
#     qty = request.json['qty']
#     price = request.json['price']
#
#     new_drink = Veg(name, image, qty, price)
#     db.session.add(new_drink)
#     db.session.commit()
#     return veg_schema.jsonify(new_drink)
#


# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

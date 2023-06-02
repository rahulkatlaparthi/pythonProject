from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

# New

# Init app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///relationship.db'

# Init database
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Create class and Model Marshmallow Schema


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, name, password):
        self.name = name
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def parse_response(success, data, message):
    return {"success": success, "data": data, "message": message}


# create a drink
@app.route('/registerUser', methods=['POST'])
def register_user():
    name = request.json['name']
    password = request.json['password']

    user = User(name, password)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user)


# Get all drinks
@app.route('/getUsers', methods=['GET'])
def get_users():
    all_drinks = User.query.all()
    result = users_schema.dump(all_drinks)
    return jsonify(result)


# Get single drink
@app.route('/getUserById/<id>', methods=['GET'])
def get_user_by_id(id):
    drink = User.query.get(id)
    return user_schema.jsonify(drink)


# Update a drink
@app.route('/updateUser/<id>', methods=['PUT'])
def update_user_drink(id):
    drink = User.query.get(id)

    name = request.json['name']
    image = request.json['image']
    qty = request.json['qty']
    price = request.json['price']

    drink.name = name
    drink.image = image
    drink.qty = qty
    drink.price = price

    db.session.commit()
    return user_schema.jsonify(drink)


# Validate a drink
@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    name = request.json['name']
    password = request.json['password']
    drink = User.query.filter_by(name=name, password=password)
    items = users_schema.dump(drink)
    print(items)
    if len(items) == 0:
        data = parse_response(success=False, data=False, message="Authentication Failed")

    else:
        data = parse_response(success=True, data=True, message="Login Success")

    return jsonify(data)


# Delete single drink
@app.route('/deleteUser/<id>', methods=['DELETE'])
def delete_user(id):
    drink = User.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    return user_schema.jsonify(drink)


# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=5000)

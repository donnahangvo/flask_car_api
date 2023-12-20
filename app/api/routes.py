from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'totally': 'tubular'}

# @api.route('/cars', methods = ['POST'])
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    color = request.json['color']
    year = request.json['year']
    vin_number = request.json['vin_number']
    user_token = current_user_token.token
    # breakpoint()
    print(current_user_token.token)
    print(f'BIG TESTER: {current_user_token}')

    car = Car(make, model, color, year, vin_number, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)


# GET method to retrieve data that has been created

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# GET method to call a specific contact with an ID number

# @api.route('/cars/<id>', methods = ['GET'])
# @token_required
# def get_single_car(current_user_token, id):
#     a_user = current_user_token.token
#     single_car = Car.query.filter_by(user_token = a_user).first()
#     response = car_schema.dump(single_car)
#     return jsonify(response)


@api.route('/cars/<id>', methods=['GET'])
@token_required
def get_single_car(current_user, id):
    a_user = current_user.token
    single_car = Car.query.filter_by(user_token=a_user, id=id).first()
    if single_car:
        response = car_schema.dump(single_car)
        return jsonify(response)
    else:
        return jsonify({"message": "Car not found"}), 404


# UPDATE endpoint
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.color = request.json['color']
    car.year = request.json['year']
    car.vin_number = request.json['vin_number']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    a_user = current_user_token.token
    single_car = Car.query.filter_by(user_token = a_user).first()
    db.session.delete(single_car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
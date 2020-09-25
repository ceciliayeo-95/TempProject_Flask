from WebApp import *
from flask import render_template, Flask, jsonify, request, make_response, flash, redirect, url_for
from WebApp.models import *
from WebApp.forms import *
import requests
import jwt
import json
import datetime
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            username = data['username']
            #current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(username, *args, **kwargs)

    return decorated

@app.route('/')
def hello_world():
    return 'Hello World! Cecilia'

@app.route('/home',methods=['GET'])
def home():
    cars = Car.query.all()
    return render_template('home.html', cars=cars)

@app.route('/protected')
@token_required
def protected(username):
    return jsonify({'message': 'This is protected', 'username':username})

@app.route('/cars',methods=['GET'])
def listCars():
    return ''

@app.route('/cars/<id>',methods=['GET'])
def listCar():
    return ''

@app.route('/cars',methods=['POST'])
def createCar():
    carName = request.args.get('carName')
    price = request.args.get('price')
    return jsonify({'carName': carName, 'price': price})

@app.route('/cars/<id>',methods=['DELETE'])
def deleteCar():
    return ''

@app.route('/apiData',methods=['GET'])
def getAPI_test():
    # sending get request and saving the response as response object
    URL = 'https://api.data.gov.sg/v1/environment/psi'
    PARAMS = {}
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.json()
    print(data['api_info'])
    return data


@app.route('/createcars',methods=['GET','POST'])
def CreateCar():
    cars = Car.query.all()
    form = CarForm()

    if form.validate_on_submit():
        carName = form.carName.data
        price = form.price.data
        car = Car(carName=carName, price=price)
        db.session.add(car)
        db.session.commit()
        flash(f'Car Created!!', 'success')
        return redirect(url_for('home'))
    return render_template('createcar.html', form=form, cars=cars)

@app.route('/onboardcustomer',methods=['GET','POST'])
def CreateCustomer():
    productTypeList = ['00 - investor', '01 - insurance', '02 - loans', '03 - savings' , '04 - credit card']
    productType_choice = []
    # Unpack to tuple
    for i in range(len(productTypeList)):
        productType_choice.append((productTypeList[i], productTypeList[i]))

    form = CustomerForm()

    if form.validate_on_submit():
        customerName = form.customerName.data
        customerDOB = form.customerDOB.data
        serviceOfficerName = form.serviceOfficerName.data
        NRIC = form.NRIC.data
        branchCode = form.branchCode.data
        productType = form.productType.data

        customer = Customer(customerName=customerName, customerDOB=customerDOB, serviceOfficerName=serviceOfficerName,NRIC=NRIC,branchCode=branchCode,productType=productType)
        print(customer)
        # db.session.add(car)
        # db.session.commit()
        flash(f'Customer: {customerName} has been sucessfully registered!!', 'success')
        #return redirect(url_for('home'))
    return render_template('createUser.html', form=form)

@app.route('/selectcars',methods=['GET','POST'])
def selectCar():
    #----------------------------------------------#
    gender = ['M','F']
    gender_choice = []
    #Unpack to tuple
    for i in range(len(gender)):
        gender_choice.append((gender[i],gender[i]))
    #----------------------------------------------#
    form = selectForm()
    form.gender.choices = gender_choice

    if form.validate_on_submit():
        car = form.opts.data
        carName = car.carName
        gender = form.gender.data

        flash(f'Car: {carName} selected, {gender}!', 'success')

    return render_template('selectcar.html', form=form)

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    # user = User.query.filter_by(name=auth.username).first()
    #
    # if not user:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    #if check_password_hash(user.password, auth.password):
    token = jwt.encode(
        {'username': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
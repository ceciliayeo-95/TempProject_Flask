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
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():

    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        res = requests.get('http://techtrek2020.ap-southeast-1.elasticbeanstalk.com/login', data={'username': form.username.data, 'password': form.password.data})
        print(res)

        # user = User.query.filter_by(email=form.email.data).first()
        # if user and bcrypt.check_password_hash(user.password, form.password.data):
        #     login_user(user, remember=form.remember.data)
        #     next_page = request.args.get('next')
        #     return redirect(next_page) if next_page else redirect(url_for('home'))
        # else:
        #     flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/home',methods=['GET'])
def home():
    customers = Customer.query.all()
    return render_template('home.html', customers=customers)

@app.route('/protected')
@token_required
def protected(username):
    return jsonify({'message': 'This is protected', 'username':username})


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

@app.route('/onboardcustomer',methods=['GET','POST'])
def CreateCustomer():
    productTypeList = ['00 - investor', '01 - insurance', '02 - loans', '03 - savings' , '04 - credit card']
    productType_choice = []
    # Unpack to tuple
    for i in range(len(productTypeList)):
        productType_choice.append((productTypeList[i], productTypeList[i]))

    form = CustomerForm()
    form.productType.choices = productType_choice

    if form.validate_on_submit():
        customerName = form.customerName.data
        customerDOB = form.customerDOB.data
        serviceOfficerName = form.serviceOfficerName.data
        NRIC = form.NRIC.data
        branchCode = form.branchCode.data
        productType = form.productType.data

        customer = Customer(customerName=customerName, customerDOB=customerDOB, serviceOfficerName=serviceOfficerName,NRIC=NRIC,branchCode=branchCode,productType=productType)
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer: {customerName} has been sucessfully registered!!', 'success')
        #return redirect(url_for('home'))
    return render_template('createUser.html', form=form)

@app.route("/customer/<int:id>/delete", methods=['POST'])
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()
    flash('Customer has been deleted!', 'success')
    return redirect(url_for('home'))


# @app.route('/login2')
# def login2():
#     auth = request.authorization
#
#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#     # user = User.query.filter_by(name=auth.username).first()
#     #
#     # if not user:
#     #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
#
#     #if check_password_hash(user.password, auth.password):
#     token = jwt.encode(
#         {'username': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
#         app.config['SECRET_KEY'])
#
#     return jsonify({'token': token.decode('UTF-8')})
#
#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
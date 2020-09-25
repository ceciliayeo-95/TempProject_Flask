from WebApp import *
from flask import render_template, Flask, jsonify, request, make_response, flash, redirect, url_for
from WebApp.models import *
from WebApp.forms import *
import requests
import jwt
import json
import datetime
from functools import wraps

token = ''

@app.route('/')
def hello_world():
    return token


@app.route('/login', methods=['GET','POST'])
def login():
    global token

    form = LoginForm()
    if form.validate_on_submit():
        res = requests.post('http://techtrek2020.ap-southeast-1.elasticbeanstalk.com/login', json={'username': form.username.data, 'password': form.password.data})
        if res.status_code != 200:
            flash('Login unsuccessful. Please check username and password', 'danger')
        else:
            token = res.content
            flash(f'Login Successful!', 'success')
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route('/home',methods=['GET'])
def home():
    customers = Customer.query.all()
    return render_template('home.html', customers=customers)


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
    productTypeList = ['137 : Investor', '070 : Insurance', '291 : Loans', '969 : Savings' , '555 : Credit Cards']
    productType_choice = []
    # Unpack to tuple
    for i in range(len(productTypeList)):
        productType_choice.append((productTypeList[i], productTypeList[i]))

    form = CustomerForm()
    #form.productType.choices = productType_choice
    form.productType2.choices = productType_choice

    if form.validate_on_submit():
        customerName = form.customerName.data
        customerAge = form.customerAge.data
        customerDOB = form.customerDOB.data
        serviceOfficerName = form.serviceOfficerName.data
        NRIC = form.NRIC.data
        branchCode = form.branchCode.data
        productType = ','.join(form.productType2.data)

        print(productType)

        customer = Customer(customerName=customerName, customerAge=customerAge,customerDOB=customerDOB, serviceOfficerName=serviceOfficerName,NRIC=NRIC,branchCode=branchCode,productType=productType)
        db.session.add(customer)
        db.session.commit()
        flash(f'Customer: {customerName} has been sucessfully registered!!', 'success')
        return redirect(url_for('home'))

    return render_template('createUser.html', form=form)

@app.route("/customer/<int:id>/delete", methods=['POST'])
def delete_customer(id):

    customer = Customer.query.get_or_404(id)

    db.session.delete(customer)
    db.session.commit()
    flash('Customer has been deleted!', 'success')
    return redirect(url_for('home'))



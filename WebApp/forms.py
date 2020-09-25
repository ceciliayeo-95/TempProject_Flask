from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from WebApp.models import *
from WebApp import db

class CustomerForm(FlaskForm):
    customerName = StringField('Customer Name', validators=[DataRequired()])
    customerDOB = StringField('Date Of Birth (DD/MM/YYYY)', validators=[DataRequired()])
    serviceOfficerName = StringField('Service Officer Name', validators=[DataRequired()])
    NRIC = StringField('NRIC', validators=[DataRequired()])
    branchCode = IntegerField('Branch Code', validators=[DataRequired()])
    productType = SelectField('Product Type', choices=[])

    submit = SubmitField('Onboard Customer')

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
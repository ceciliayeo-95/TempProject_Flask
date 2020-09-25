from flask_wtf import FlaskForm
from wtforms import IntegerField,StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from WebApp.models import *
from WebApp import db

class CarForm(FlaskForm):
    carName = StringField('Car Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Create Car')

def choice_query():
    return Car.query

class selectForm(FlaskForm):
    opts = QuerySelectField('Select Choice', query_factory=choice_query, allow_blank=False, get_label='carName')
    gender = SelectField('Category', choices=[])
    submit = SubmitField('Select Car')

class CustomerForm(FlaskForm):
    customerName = StringField('Customer Name', validators=[DataRequired()])
    customerDOB = StringField('Date Of Birth (DD/MM/YYYY)', validators=[DataRequired()])
    serviceOfficerName = StringField('Service Officer Name', validators=[DataRequired()])
    NRIC = StringField('NRIC', validators=[DataRequired()])
    branchCode = IntegerField('Branch Code', validators=[DataRequired()])
    productType = StringField('Product Type', validators=[DataRequired()])

    submit = SubmitField('Onboard Customer')

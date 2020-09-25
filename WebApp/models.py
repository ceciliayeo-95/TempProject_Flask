from WebApp import db

class Customer(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    customerName = db.Column(db.String(100))
    customerAge = db.Column(db.INTEGER)
    customerDOB = db.Column(db.String(50))
    serviceOfficerName = db.Column(db.String(50))
    NRIC = db.Column(db.String(20))
    registrationTime = db.Column(db.String(50), default="25/09/20 00:00:00")
    branchCode = db.Column(db.INTEGER)
    productType = db.Column(db.String(100))


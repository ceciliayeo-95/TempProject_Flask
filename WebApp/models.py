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



# customerName: string maxlen(64) a-zA-Z
#
#     customerAge: integer (> 18)
#
#     customerDOB: DD/MM/YYYY
#
#     serviceOfficerName: string
#
#     NRIC: string - all caps [A-Z][0-9]{7}[A-Z]
#     registrationTime: DD/MM/YY HH:mm:SS
#
#     branchCode: integer
#
#     image: blob (max size 2MB) optional
#
#     productType: array[string] 00 - investor, 01 - insurance, 02 -
# loans, 03 - savings, 04 - credit card (idk)

from WebApp.models import *

try:
    db.drop_all()
except:
    pass

db.create_all()
customer = Customer(customerName="Cecilia", customerDOB='01/01/1995', serviceOfficerName='OfficerA',NRIC='S9521678E',branchCode=1,productType='02 - loans')

db.session.add(customer)
db.session.commit()

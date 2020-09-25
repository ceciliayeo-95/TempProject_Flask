from WebApp.models import *

try:
    db.drop_all()
except:
    pass

db.create_all()

car_1 = Car(carName='Honda',price = 1000)
car_2 = Car(carName='Toyata',price = 2000)
customer = Customer(customerName="Cecilia", customerDOB='01/01/1995', serviceOfficerName='OfficerA',NRIC='S9521678E',branchCode=1,productType='02 - loans')

db.session.add(car_1)
db.session.add(car_2)
db.session.add(customer)
db.session.commit()

print(Car.query.all())

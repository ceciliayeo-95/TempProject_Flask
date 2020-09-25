from WebApp.models import *

try:
    db.drop_all()
except:
    pass

db.create_all()

car_1 = Car(carName='Honda',price = 1000)
car_2 = Car(carName='Toyata',price = 2000)

db.session.add(car_1)
db.session.add(car_2)
db.session.commit()

print(Car.query.all())

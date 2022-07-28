from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

bob = User(first_name='bob', last_name='ross', image_url='https://yt3.ggpht.com/ytc/AKedOLSRSl8xsTNuQU_f6sg3bHI19gZYUSqLu2I78S90MQ=s900-c-k-c0x00ffffff-no-rj')
david = User(first_name='david', last_name='grong')
katie = User(first_name='katie', last_name='grong')

db.session.add(bob)
db.session.add(david)
db.session.add(katie)

db.session.commit()
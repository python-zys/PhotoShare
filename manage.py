#-*- encoding=UTF-8 -*-
from nowstagram import app,db
from flask_script import Manager
from nowstagram.models import User,Image,Comment
import datetime
import random

manager = Manager(app)

def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 1000)) + 'm.png'

@manager.command
def init_database():
    db.drop_all()
    db.create_all()
    for i in range(0,100):
        db.session.add(User('User'+str(i), 'a'+str(i)))
        for j in range(0,3):
            db.session.add(Image(get_image_url(), i+1))
            for k in range(0,3):
                db.session.add(Comment('this is comment '+str(k), int(1+3*i+j), int(i+1)))
    db.session.commit()

    print 1, User.query.all()
    print 2, User.query.get(3)

if __name__ == '__main__':
    manager.run()


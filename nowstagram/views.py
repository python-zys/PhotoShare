#-*- encoding=UTF-8 -*-
from nowstagram import db
from nowstagram import app
from models import Image, User
from flask import render_template, redirect

@app.route('/')
def index():
    images = Image.query.order_by(db.desc(Image.id)).limit(10).all()
    return render_template('index.html', images = images)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Flower(db.Model):
    __tablename__ = 'flower'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    meaning = db.Column(db.Text, nullable=False)
    greeting = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(256))

class Occasion(db.Model):
    __tablename__ = 'occasion'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    suggestion_list = db.Column(db.Text)
    greeting = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(256))
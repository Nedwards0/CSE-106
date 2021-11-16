
from flask import Flask, request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True)
    name=db.Column(db.String(30))
    passwrod=db.Column(db.String(30))
    types=db.Column(db.String(30))
    def __init__(self, username, password,name,type):
        self.username = username
        self.password = password
        self.name=name
        self.types=type
    def get_pass(self, password):
        return self.password == password

class Classes(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    name= db.Column(db.String(30))
    enrolled=db.Column(db.Integer)
    maxenrolled=db.Column(db.Integer)
    type = db.Column(db.Integer, nullable = False)

class Enroll(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'),nullable=False)




@app.route('/')
def hello_world():
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True

    app.run()   
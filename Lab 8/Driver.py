
from flask import Flask, request, render_template,jsonify,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user

app = Flask(__name__) 
app.secret_key = 'ASDASDDASDSAFA'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(30),unique=True)
    name=db.Column(db.String(30))
    password=db.Column(db.String(30))
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
    enrolled=db.Column(db.Integer)





@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        user=request.form['username']
        passs=request.form['password']
    try:
        session.pop('user_id', None)
        user=User.query.filter_by(username=user).first()
        if(user.password==passs):
            print(user.types)
            session['user_id'] = user.id
            if(int(user.types)==1):
                print("ADMIN")
                return redirect('admin')#NEEDS TO BE IMPLEMENTED
            if(user.types==2):
                print("STUDENT")
                return redirect("student")#NEEDS TO BE IMPLEMENTED
            if(user.types==3):
                print("TEACHER")
                return redirect("teacher")#NEEDS TO BE IMPLEMENTED
            

        else:
            print("FAIL")
    except:
        print("User does not exist")
    return render_template("login.html")


if __name__ == '__main__':
    app.debug = True

    app.run()   

from flask import Flask, request, render_template,jsonify,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_login import login_required, logout_user, login_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__) 
app.secret_key = 'ASDASDDASDSAFA'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)
login=LoginManager(app)
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
    teacher_id = db.Column(db.Integer)
    name= db.Column(db.String(30))
    enrolled=db.Column(db.Integer)
    maxenrolled=db.Column(db.Integer)
    type = db.Column(db.Integer, nullable = False)
class Enroll(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    enrolled=db.Column(db.Integer)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class adminview(ModelView):
    def is_accessible(self):
        print(current_user.types)
        if(int(current_user.types)==1):
            print("TRUE")
            return current_user.is_authenticated
        else:
            return False
    def inaccessible_callback(self, name, **kwargs):
        return redirect("login")
class studentview(ModelView):
    pass
class Teacherview(ModelView):
    pass
admin=Admin(app)
admin.add_view(adminview(User,db.session))
admin.add_view(adminview(Classes,db.session))
admin.add_view(adminview(Enroll,db.session))


@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=="POST"):
        user=request.form['username']
        passs=request.form['password']
    try:
        session.pop('user_id', None)
        user=User.query.filter_by(username=user).first()
        if(user.password==passs):
            session['user_id'] = user.id
            print(user.types)
            login_user(user)
            if(int(user.types)==1):
                print("ADMIN")
                return redirect('admin')
            if(int(user.types)==2):
                print("STUDENT")
                return redirect("/student")
            if(int(user.types)==3):
                print("TEACHER")
                return redirect("/teacher")
        else:
            print("FAIL")
    except:
        print("User does not exist")
    return render_template("login.html")

class classes():
    grade=0
    teacher='0'
    name=''
    time=''
    enrolled=''
    max_enrolled=''
    def __init__(self,grade,teacher,name,enrolled,max_enrolled):
        self.grade=grade
        self.teacher=teacher
        self.name=name
        self.enrolled=enrolled
        self.max_enrolled=max_enrolled



@app.route('/student',methods=['GET'])
def student():
    if(request.method=='GET'):
        return render_template("student.html")

@app.route('/student/data')
def return_data():
    session_id = session['user_id']
    user_id = Enroll.query.filter_by(user_id = session_id).all()
    grades=[]
    class_id=[]
    stud_class=[]
    for enroll in user_id:
        class_id.append(enroll.class_id)
        grades.append(enroll.enrolled) 
    for i,clas in enumerate(class_id):
        c=Classes.query.filter_by(id=clas).first()
        teacher=User.query.filter_by(id=c.teacher_id).first()
        teacher=teacher.name
        cure_classes= [{'grades': grades[i]},{'teacher': teacher},{'class_name':  c.name},{'enrolled': c.enrolled},{'max_enrolled': c.maxenrolled}]
        stud_class.append(cure_classes)
        
    return jsonify(stud_class)

@app.route('/student/classes')
def all_classes():
    
    return jsonify(data)


    

@app.route('/teacher',methods=['GET'])
def teacher():
    if(request.method=='GET'):
        return render_template("teacher.html")

@app.route('/logout', methods=['POST'])
@ login_required
def logout():
    logout_user()
    return render_template('login.html')

if __name__ == '__main__':
    app.debug = True

    app.run()   
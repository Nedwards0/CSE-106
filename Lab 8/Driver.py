
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
    date=db.Column(db.String(30))
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
        cure_classes= [{'grades': grades[i]},{'teacher': teacher},{'class_name':  c.name},{'enrolled': c.enrolled},{'max_enrolled': c.maxenrolled},{'time':c.date}]
        stud_class.append(cure_classes)     
        
    return jsonify(stud_class)

@app.route('/student/classes')
def all_classes():
    session_id = session['user_id']
    all_classes=[]
    test=Classes.query.all()    
    for c in test:
        teacher=User.query.filter_by(id=c.teacher_id).first()
        teacher=teacher.name
        a=[{'teacher': teacher},{'class_name':  c.name},{'enrolled': c.enrolled},{'max_enrolled': c.maxenrolled},{'time':c.date}]
        all_classes.append(a)
    return(jsonify(all_classes))

#return list of classes 
@app.route('/teacher/classes')
def proff_classes():
    session_id = session['user_id']
    q=Classes.query.filter_by(teacher_id=session_id).all()
    b=[]
    print(q)
    for c in q:
        a=[{'class_id':c.id},{'class_name':  c.name},{'enrolled': c.enrolled},{'max_enrolled': c.maxenrolled}]
        b.append(a)
    print(b)
    return(jsonify(b))


#class object with all class info
@app.route('/teacher/<string:class_id>')
def proff_classe(class_id):
    print(class_id)
    c=Enroll.query.filter_by(class_id=class_id).all()
    outs=[]
    for k in c:
        id=k.user_id
        user=User.query.get(id)
        a=[{'stud_id':user.id},{'name':user.name},{"grade":k.enrolled},{"class_id":class_id}]
        outs.append(a)
    return (jsonify(outs))
@app.route('/student/g/<string:class_id>')
def add_todb(class_id):
    class_id=3
    try:
        c=Enroll.query.filter_by(user_id=session['user_id'])
        for k in c:
            if k.class_id==class_id:
                print(k)
                clas=Classes.query.filter_by(id=class_id).first()
                clas.enrolled=clas.enrolled-1
                db.session.delete(k)
                db.session.commit()
                return "s"
    except:
        pass
    print("AAAA")
    c=Enroll.query.filter_by(class_id=class_id).first()
    clas=Classes.query.filter_by(id=class_id).first()
    clas.enrolled=clas.enrolled+1
    class_id=c.class_id
    enroll=Enroll(user_id=session['user_id'],class_id=class_id,enrolled=99)
    db.session.add(enroll)
    db.session.commit()
    return "s"
@app.route('/student/add_class/<string:class_id>')
def proff_classez(class_id):
    print(class_id)
    
    c=Classes.query.get(class_id)
    a=[{'id':c.id},{'name':c.name},{'enrolled':c.enrolled},{'max':c.maxenrolled}]
    return (jsonify(a))

@app.route('/teacher',methods=['GET'])
def teacher():
    if(request.method=='GET'):
        users=Classes.query.filter_by(teacher_id=session['user_id']).all()

        return render_template("teacher.html",users=users)
class temp():
    grade=0
    name=0
    id=0
    clas=0
    def __init__(self,grade,name,id,clas):
        self.grade=grade
        self.name=name
        self.id=id
        self.clas=clas
@app.route('/teacher/setter/<student>/<class_id>')
def set(student,class_id):
    grade=request.args.get("grade")
    print(student,class_id,grade)
    student=int(student)
    a=Enroll.query.filter_by(user_id=student)
    for k in a:
        if k.class_id==int(class_id):
            print(k.enrolled)
            print(k)
            break
    enroll=Enroll.query.get(k.id)
    enroll.enrolled=int(grade)
    db.session.commit()
    return redirect('/teacher')
@app.route('/teacher/all/<class_id>')
def all(class_id):
    print(class_id)
    a=Enroll.query.filter_by(class_id=class_id)
    users=[]
    for c in a:
        user_id=c.user_id
        j=User.query.filter_by(id=user_id).first()
        users.append(temp(c.enrolled,j.name,j.id,c.class_id))

    return render_template("all.html",users=users)
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if(request.method=='GET'):
        logout_user()
        return redirect('/login')

if __name__ == '__main__':
    app.debug = True

    app.run()   
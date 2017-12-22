from flask import Flask, redirect, url_for, request, render_template, flash, session
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))  
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr,pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

class LoginForm(Form):
    userName = StringField('User name:', validators = [Required("Please enter user name")])
    passWord = StringField('PassWord:', validators = [Required("Please enter password")])

class StudentForm(Form):
    name = StringField("Student Name: ", validators = [Required("Please enter student name")])
    city = StringField("City: ", validators = [Required("Please enter city")])
    address = StringField("Address: ", validators = [Required("Please enter address")])
    pin = StringField("Pin code: ", validators = [Required("Please enter pin code")])

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods = ['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        userName = request.form['userName']
        passWord = request.form['passWord']
        if(userName != 'DungNT57' or passWord != '123456' ):
            flash('User name or password is invalid')
            return render_template('login.html',form = form)
        else:
            session['userName'] = userName
            return redirect(url_for('students'))
    else:
        return render_template('login.html',form = form)

@app.route('/logout')
def logout():
    session.pop('userName', None)
    return redirect(url_for('index'))

@app.route('/students')
def students():
    return render_template('students.html', students = Students.query.all())

@app.route('/students/new',methods = ['POST', 'GET'])
def new():
    if(session['userName'] is None)
    form = StudentForm(request.form)
    if request.method == 'POST' and form.validate():
        student = Students(request.form['name'], request.form['city'],
            request.form['address'], request.form['pin'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))
    else:
        return render_template('new_student.html', form = form)

@app.route('/students/delete',methods = ['Post'])
def delete():
    student = Students.query.filter(Students.id == request.form['id']).first()
    if(student is not None):
        db.session.delete(student);
        db.session.commit()
    return redirect(url_for('students'))
    
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()
    app.config['DEBUG'] = True
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import UniqueConstraint

db=SQLAlchemy()

class Attendance(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'),nullable=False)
    date=db.Column(db.Date,default=datetime.now)
    status= db.Column(db.String(10),nullable=False,default='Present')
    student = db.relationship('Student',backref='attendances')

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    roll_no=db.Column(db.Integer,unique=True,nullable=False)
    course=db.Column(db.String(30))
    password=db.Column(db.String(100))
    def __init__(self,name,roll_no,password,course):
        self.name = name
        self.roll_no = roll_no
        self.password = password
        self.course = course
        
class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    is_active=db.Column(db.Boolean,default=False)


class Contact(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    message=db.Column(db.Text,nullable=False)
    date=db.Column(db.DateTime,default=datetime.now)
    def __init__(self,name,email,message):
        self.name = name
        self.email = email
        self.message = message
        self.date = datetime.now()

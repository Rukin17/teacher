from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'groups'
    
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable = True)
    
    def __repr__(self):
        return f'<class {self.id}>'
    

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable = True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    
    group = relationship("Group", backref="students")

    def __repr__(self):
        return f'<student {self.id}>' 
    

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50), nullable = True)

    def __repr__(self):
        return f'<course {self.id}>'


class Estimate(db.Model):
    __tablename__ = 'estimates'

    id = db.Column(db.Integer, primary_key=True)
    estimate = db.Column(db.String(50), nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    student = relationship('Student', backref='estimates')
    course = relationship('Course', backref='estimates')

    def __repr__(self):
        return f'<estimate {self.id}>'
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'group'
    
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable = True)
    
    def __repr__(self):
        return f'<class {self.id}>'
    

class Student(db.Model):
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable = True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    
    group = relationship("Group", backref="student")

    def __repr__(self):
        return f'<student {self.id}>' 
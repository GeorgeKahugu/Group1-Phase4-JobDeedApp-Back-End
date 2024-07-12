from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True, nullable = False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.String(20),nullable=False)

    job = db.relationship('Job', backref='applicants', lazy=True)
    # applications = db.relationship('Application', backref='applicant', lazy=True)

def __repr__(self):
    return f"<Applicant {self.id}: {self.username}>"


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company= db.Column(db.String(120),nullable=False)
    location=db.Column(db.String(120), nullable=False)
    employer_id=db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

def __repr__(self):
    return f"<Job {self.id}: {self.title}>"




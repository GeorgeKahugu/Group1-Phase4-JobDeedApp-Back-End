from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True, nullable = False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20),nullable=False)
    jobs = db.relationship('Job', backref='employer', lazy=True)
    applications = db.relationship('Application', backref='applicant', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company= db.Column(db.String(120),nullable=False)
    location=db.Column(db.String(120), nullable=False)
    employer_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    applications=db.relationship('Application', backref='job',lazy=True)
    reviews=db.relationship('Review', backref='job', lazy=True)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id=db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status=db.Column(db.String(20), nullable=False)
    date_applied=db.Column(db.DateTime, nullable=False)









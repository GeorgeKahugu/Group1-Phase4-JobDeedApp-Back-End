from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Applicant(db.Model, SerializerMixin):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True, nullable = False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.String(20),nullable=False)

    jobs = db.relationship('Job', back_populates='applicant')
    # applications = db.relationship('Application', backref='applicant', lazy=True)

def __repr__(self):
    return f"<Applicant {self.id}: {self.username}>"


class Job(db.Model, SerializerMixin):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company= db.Column(db.String(120),nullable=False)
    location=db.Column(db.String(120), nullable=False)
    employer_id=db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    applicant = db.relationship('Applicant', back_populates='jobs')

def __repr__(self):
    return f"<Job {self.id}: {self.title}>"



class Applications(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id=db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status=db.Column(db.String(20), nullable=False)
    date_applied=db.Column(db.DateTime, nullable=False)

#  jobs = db.relationship('Job', back_populates='applicants')

def __repr__(self):
    return f"Applications {self.id}: {self.user_id}>"

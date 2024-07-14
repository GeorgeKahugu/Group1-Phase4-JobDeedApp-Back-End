from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from datetime import datetime

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.String(20), nullable=False)

    jobs = db.relationship('Job', back_populates='applicant')
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def __repr__(self):
        return f"<Applicant {self.id}: {self.username}>"

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'role': self.role,
           
        }


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    applicant = db.relationship('Applicant', back_populates='jobs')
    applications = db.relationship('Application', backref='job', lazy=True)

    def __repr__(self):
        return f"<Job {self.id}: {self.title}>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'location': self.location,
            'employer_id': self.employer_id,
            'created_at': self.created_at.isoformat(),
            
        }


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey('applicants.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    date_applied = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    # applicant = db.relationship("Applicant", back_populates="applications")
    # job = db.relationship("Job", back_populates="applications")

    def __repr__(self):
        return f"Application {self.id}: {self.applicant_id} - {self.job_id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'applicant_id': self.applicant_id,
            'job_id': self.job_id,
            'status': self.status,
            'date_applied': self.date_applied.isoformat() if self.date_applied else None
            
        }

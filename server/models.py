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

    # jobs = db.relationship('Job', backref='applicants', lazy=True)
    # applications = db.relationship('Application', backref='applicant', lazy=True)

def __repr__(self):
    return f"<Applicant {self.id}: {self.username}>"




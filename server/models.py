from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates
import bcrypt
import logging



# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with custom metadata
metadata = MetaData()
db = SQLAlchemy(app, metadata=metadata)

# Logging configuration
logging.basicConfig(level=logging.DEBUG)

# Models definition
class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    role = db.Column(db.String(20), nullable=False)

    jobs = db.relationship('Job', back_populates='applicant')
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def __init__(self, **kwargs):
        super(Applicant, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.password = kwargs['password']

    @hybrid_property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @validates('username')
    def validate_username(self, key, username):
        assert len(username) <= 80, "Username must be less than 80 characters"
        return username

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email format"
        return email

    @validates('role')
    def validate_role(self, key, role):
        valid_roles = ['Software Developer', 'DevOps Engineer', 'Accountant', 'Data Scientist', 'UX/UI Designer']
        if role not in valid_roles:
            raise ValueError(f"Invalid role: {role}")
        return role

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

    @validates('title', 'company', 'location')
    def validate_string_length(self, key, value):
        max_lengths = {'title': 120, 'company': 120, 'location': 120}
        if len(value) > max_lengths.get(key, 120):
            raise ValueError(f"{key.capitalize()} must be less than {max_lengths.get(key, 120)} characters")
        return value

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
    date_applied = db.Column(db.DateTime, nullable=False, default=db.func.utcnow())

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['Pending', 'Accepted', 'Rejected']
        assert status in valid_statuses, f"Invalid status: {status}"
        return status

    def __repr__(self):
        return f"Application {self.id}: {self.applicant_id} - {self.job_id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'applicant_id': self.applicant_id,
            'job_id': self.job_id,
            'status': self.status,
            'date_applied': self.date_applied.isoformat() if self.date_applied else None,
        }


# Routes
@app.route('/applicants', methods=['POST'])
def create_applicant():
    data = request.json
    try:
        new_applicant = Applicant(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            role=data['role']
        )
        db.session.add(new_applicant)
        db.session.commit()
        return jsonify(new_applicant.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating applicant: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

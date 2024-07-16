from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

from datetime import datetime
import re
from models import db, Applicant, Job, Application

# Initialize the Flask Application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret"

# Allow requests from all the origins
CORS(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Index(Resource):
    def get(self):
        body = {"index": "Welcome to JobDeed!"}
        return make_response(body, 200)

api.add_resource(Index, '/')

class Applicants(Resource):
    # @jwt_required()
    def get(self):
        # current_applicant = get_jwt_identity()
        # print(current_applicant)
        applicants = Applicant.query.all()
        applicants_list = [applicant.to_dict() for applicant in applicants]

        body = {
            "count": len(applicants_list),
            "applicants": applicants_list
        }

        return make_response(body, 200)
    
    def post(self):
        # Check if email is already taken
        email = Applicant.query.filter_by(email=request.json.get('email')).first()

        if email:
            return make_response({"message": "Email already taken"}, 422)
        
        # Validate input
        username = request.json.get("username")
        email = request.json.get("email")
        password = request.json.get("password")
        role = request.json.get("role")

        if not username or len(username) > 80:
            return make_response({"message": "Username must be between 1 and 80 characters"}, 400)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return make_response({"message": "Invalid email format"}, 400)
        if not password or len(password) < 8:
            return make_response({"message": "Password must be at least 8 characters long"}, 400)
        valid_roles = ['Software Developer', 'DevOps Engineer', 'Accountant', 'Data Scientist', 'UX/UI Designer']
        if role not in valid_roles:
            return make_response({"message": f"Invalid role: {role}"}, 400)

        new_applicant = Applicant(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
            role=request.json.get("role")
        )

        db.session.add(new_applicant)
        db.session.commit()

        access_token = create_access_token(identity=new_applicant.id)

        response = {
            "applicant": new_applicant.to_dict(),
            "access_token": access_token
        }

        return make_response(response, 201)

api.add_resource(Applicants, '/applicants')

class ApplicantResource(Resource):
    def get(self, id):
        applicant = Applicant.query.get(id)

        if applicant is None:
            return {"message": "Applicant not found"}, 404

        return applicant.to_dict(), 200

    def patch(self, id):
        applicant = Applicant.query.filter_by(id=id).first()

        if not applicant:
            return {"message": "Applicant not found"}, 404

        for attr in request.json:
            if attr == 'created_at':
                try:
                    date_value = datetime.fromisoformat(request.json.get(attr))
                    setattr(applicant, attr, date_value)
                except ValueError:
                    return {"message": "Invalid datetime format for 'created_at'"}, 400
            else:
                if attr == "username" and len(request.json.get(attr)) > 80:
                    return {"message": "Username must be less than 80 characters"}, 400
                if attr == "email" and not re.match(r"[^@]+@[^@]+\.[^@]+", request.json.get(attr)):
                    return {"message": "Invalid email format"}, 400
                if attr == "role":
                    valid_roles = ['Software Developer', 'DevOps Engineer', 'Accountant', 'Data Scientist', 'UX/UI Designer']
                    if request.json.get(attr) not in valid_roles:
                        return {"message": f"Invalid role: {request.json.get(attr)}"}, 400
                setattr(applicant, attr, request.json.get(attr))

        db.session.add(applicant)
        db.session.commit()

        return applicant.to_dict(), 200

    def delete(self, id):
        applicant = Applicant.query.get(id)

        if not applicant:
            return {"message": "Applicant not found"}, 404

        applications = Application.query.filter_by(applicant_id=id).all()
        for application in applications:
            db.session.delete(application)

        db.session.delete(applicant)
        db.session.commit()

        return {"delete_successful": True, "message": "Applicant and related applications deleted."}, 200

api.add_resource(ApplicantResource, '/applicants/<int:id>')

class Jobs(Resource):
    def get(self):
        jobs = Job.query.all()
        jobs_list = [job.to_dict() for job in jobs]

        body = {
            "count": len(jobs_list),
            "jobs": jobs_list
        }

        return make_response(body, 200)

    def post(self):
        data = request.get_json()
        
        title = data.get("title")
        company = data.get("company")
        location = data.get("location")
        description = data.get("description")
        employer_id = data.get("employer_id")

        if not title or len(title) > 120:
            return make_response({"message": "Title must be between 1 and 120 characters"}, 400)
        if not company or len(company) > 120:
            return make_response({"message": "Company must be between 1 and 120 characters"}, 400)
        if not location or len(location) > 120:
            return make_response({"message": "Location must be between 1 and 120 characters"}, 400)

        new_job = Job(
            title=title,
            description=description,
            company=company,
            location=location,
            employer_id=employer_id
        )

        db.session.add(new_job)
        db.session.commit()

        response = make_response(new_job.to_dict(), 201)

        return response

api.add_resource(Jobs, '/jobs')

class JobResource(Resource):
    def get(self, id):
        job = Job.query.get(id)

        if job is None:
            return {"message": "Job not found"}, 404

        return job.to_dict(), 200

    def patch(self, id):
        job = Job.query.filter_by(id=id).first()

        if not job:
            return {"message": "Job not found"}, 404

        for attr in request.json:
            if attr == 'created_at':
                try:
                    date_value = datetime.fromisoformat(request.json.get(attr))
                    setattr(job, attr, date_value)
                except ValueError:
                    return {"message": "Invalid datetime format for 'created_at'"}, 400
            else:
                if attr == "title" and len(request.json.get(attr)) > 120:
                    return {"message": "Title must be less than 120 characters"}, 400
                if attr == "company" and len(request.json.get(attr)) > 120:
                    return {"message": "Company must be less than 120 characters"}, 400
                if attr == "location" and len(request.json.get(attr)) > 120:
                    return {"message": "Location must be less than 120 characters"}, 400
                setattr(job, attr, request.json.get(attr))

        db.session.add(job)
        db.session.commit()

        return job.to_dict(), 200

    def delete(self, id):
        job = Job.query.get(id)

        if not job:
            return {"message": "Job not found"}, 404

        applications = Application.query.filter_by(job_id=id).all()

        for application in applications:
            db.session.delete(application)

        db.session.delete(job)
        db.session.commit()

        return {"delete_successful": True, "message": "Job and related applications deleted."}, 200

api.add_resource(JobResource, '/jobs/<int:id>')

class Applications(Resource):
    def get(self):
        applications = Application.query.all()
        applications_list = [application.to_dict() for application in applications]

        body = {
            "count": len(applications_list),
            "applications": applications_list
        }

        return make_response(body, 200)

    def post(self):
        applicant_id = request.json.get("applicant_id")
        job_id = request.json.get("job_id")
        status = request.json.get("status")
        date_applied_str = request.json.get("date_applied")

        if status not in ['Pending', 'Accepted', 'Rejected']:
            return make_response({"message": f"Invalid status: {status}"}, 400)

        if date_applied_str:
            try:
                date_applied = datetime.fromisoformat(date_applied_str)
            except ValueError:
                return make_response({"message": "Invalid datetime format for 'date_applied'"}, 400)
        else:
            date_applied = datetime.now()

        new_application = Application(
            applicant_id=applicant_id,
            job_id=job_id,
            status=status,
            date_applied=date_applied
        )

        db.session.add(new_application)
        db.session.commit()

        response = make_response(new_application.to_dict(), 201)

        return response

api.add_resource(Applications, '/applications')

class ApplicationDetailResource(Resource):
    def get(self, id):
        application = Application.query.get(id)

        if application is None:
            return {"message": "Application not found"}, 404

        return application.to_dict(), 200

    def patch(self, id):
        application = Application.query.filter_by(id=id).first()

        if not application:
            return {"message": "Application not found"}, 404

        for attr in request.json:
            if attr == 'date_applied':
                try:
                    date_value = datetime.fromisoformat(request.json.get(attr))
                    setattr(application, attr, date_value)
                except ValueError:
                    return {"message": "Invalid datetime format for 'date_applied'"}, 400
            else:
                if attr == "status" and request.json.get(attr) not in ['Pending', 'Accepted', 'Rejected']:
                    return {"message": f"Invalid status: {request.json.get(attr)}"}, 400
                setattr(application, attr, request.json.get(attr))

        db.session.add(application)
        db.session.commit()

        return application.to_dict(), 200

    def delete(self, id):
        application = Application.query.get(id)

        if not application:
            return {"message": "Application not found"}, 404

        db.session.delete(application)
        db.session.commit()

        return {"delete_successful": True, "message": "Application deleted."}, 200

api.add_resource(ApplicationDetailResource, '/applications/<int:id>')

def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(port=5555, debug=True)

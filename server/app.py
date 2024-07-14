from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS

from datetime import datetime
from models import db, Applicant, Job ,Application

#Initialize the Flask Application
app = Flask(__name__)

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "super-secret"

#Allow requests from all the origins
CORS(app)

bcrypt=Bcrypt(app)
jwt=JWTManager(app)


migrate= Migrate(app, db)
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
        #check if email is already taken 
        email = Applicant.query.filter_by(email=request.json.get('email')).first();

        if email:
            return make_response ({"message":"Email already taken"}, 422)
        new_applicant = Applicant(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=bcrypt.generate_password_hash(request.json.get("password")),
            role=request.json.get("role")
        )

        db.session.add(new_applicant)
        db.session.commit()

        access_token = create_access_token(identity=new_applicant.id)

        response = {
            "applicant": new_applicant.to_dict(),
            "access_token": access_token 
        }

        response = make_response(response, 201)

        return response

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
        new_job = Job(
            title=request.json.get("title"),
            description=request.json.get("description"),
            company=request.json.get("company"),
            location=request.json.get("location"),
            employer_id=request.json.get("employer_id")
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
                setattr(job, attr, request.json.get(attr))

        db.session.add(job)
        db.session.commit()

        return job.to_dict(), 200

    def delete(self, id):
        job = Job.query.get(id)

        if not job:
            return {"message": "Job not found"}, 404
        
        applications=Application.query.filter_by(job_id=id).all()

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
        
        date_applied_str = request.json.get("date_applied")
        if date_applied_str:
            try:
                date_applied = datetime.fromisoformat(date_applied_str)
            except ValueError:
                return {"message": "Invalid datetime format for 'date_applied'"}, 400
        else:
            date_applied = datetime.now()
        

        new_application = Application(
            applicant_id=request.json.get("applicant_id"),
            job_id=request.json.get("job_id"),
            status=request.json.get("status"),
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
    


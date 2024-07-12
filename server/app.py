from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from models import db, Applicant, Job     

# ,Application

#Initialize the Flask Application
app = Flask(__name__)

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

migrate= Migrate(app, db)
db.init_app(app)

api = Api(app)


class Index(Resource):
    def get(self):
        body = {
            "index":"Welcome to The Job Application App!"
        }
        response = make_response(body, 200)

        return response
    
api.add_resource(Index, '/')

class Applicants(Resource):
    def get(self):
        applicants = Applicant.query.all()
        applicants_list= []

        for applicant in applicants:
            applicants_list.append(applicant.to_dict())

        body = {
            "count": len(applicants_list),
            "applicants": applicants_list
        }

        return make_response(body,200)
    
    def post(self):
        new_applicant=Applicant(
            username=request.json.get("username"),
            email=request.json.get("email")
        )

        db.session.add(new_applicant)
        db.session.commit()

        response = make_response(new_applicant.to_dict(), 201)

        return response

api.add_resource(Applicants, '/applicants')

class ApplicantResource(Resource):
    def get(self, id):
        applicant = Applicant.query.get(id)

        if applicant is None:
            return {"message": "Applicant not found"}, 404
        return {"id": applicant.id, "username": applicant.username}, 200

    def patch(self, id):
        applicant = Applicant.query.filter_by(id=id).first()

        if not applicant:
            return {"message": "Applicant not found"}, 404

        for attr in request.json:
            setattr(applicant, attr, request.json.get(attr))

        db.session.add(applicant)
        db.session.commit()

        applicant_dict = applicant.to_dict()
        response = make_response(applicant_dict, 200)

        return response

    def delete(self, id):
        applicant = Applicant.query.get(id)
        if applicant is None:
            return {"message": "Applicant not found"}, 404

        db.session.delete(applicant)
        db.session.commit()

        body = {
            "delete_successful": True,
            "message": "Applicant deleted."
        }

        response = make_response(body, 200)
        return response

api.add_resource(ApplicantResource, '/applicants/<int:id>')

def create_tables():
    db.create_all()





if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


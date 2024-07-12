from flask import Flask, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS


from models import db, Applicant, Job     

# Job, Application

#Initialize the Flask Application
app = Flask(__name__)

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)

migrate= Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    return '<h1>Welcome to The Job Application App!</h1>'

@app.route('/applicants')
def all_applicants():
    applicants = Applicant.query.all()
    applicants_list=[]
    
    for applicant in applicants:

        applicant_dict= {
            "id": applicant.id,
            "username": applicant.username,
            "email": applicant.email,
            "password": applicant.password,
            "created_at": applicant.created_at,
            "role": applicant.role

        }
        applicants_list.append(applicant_dict)

    body = {
        "count": len(applicants),
        "applicants": applicants_list

    }

    response = make_response(body, 200)

    return response

@app.route('/applicants/<int:id>')
def get_applicant(id):
    applicant = Applicant.query.filter_by(id=id).first()

    if applicant:
        body = {
            "id": applicant.id,
            "username": applicant.username,
            "email": applicant.email,
            "password": applicant.password,
            "created_at": applicant.created_at,
            "role": applicant.role
        }
        status = 200
    else:
        body = {
            "message" f"Applicant id{id} not found."
        }
        status = 404

    return make_response(body, status)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


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
    response_body=f"<h2>List of all Applicants</h2>"

    for applicant in applicants:
        response_body+=f"<p>{applicant.username}</p>"

    response = make_response(response_body, 200)

    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


from app import app
from models import db, Applicant

with app.app_context():

    #Empty list of applicants
    applicants = []

    applicants.append(Applicant(username="Jacob Wilson", email="jacobwilson@email.com", password="6542318",role="Accountant"))
    applicants.append(Applicant(username="Jane Doe", email="janedoe@email.com",password="9783421", role="DevOps Engineer" ))

    db.session.add_all(applicants)
    db.session.commit()
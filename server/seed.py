from faker import Faker
from app import app
from models import db, Applicant

with app.app_context():
    fake=Faker()

    #Delete all records/rows in the applicants table
    Applicant.query.delete()

    #Empty list of applicants
    applicants = []

    roles = ['Software Developer', 'DevOps Engineer', 'Accountant', 'DataScientist']

    for _ in range(10):
        username=fake.user_name()
        domain=fake.free_email_domain()
        email=f"{username}@{domain}"
        password=fake.password()
        role= fake.random.choice(roles)
        
    
        applicants.append(Applicant(username=username, email=email, password=password, role=role))


    
    db.session.add_all(applicants)
    db.session.commit()
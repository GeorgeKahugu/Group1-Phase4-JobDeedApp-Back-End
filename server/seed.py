from models import Application, db, Job, Applicant
from app import app
from datetime import datetime 
from faker import Faker
from flask_bcrypt import generate_password_hash


def seed_data():
    fake = Faker()

    with app.app_context():

    #Drop all tables and create them

        db.drop_all()
        db.create_all()
   
         # Seed Users
        applicants = []
        for _ in range(5):
            applicant = Applicant(
                username=fake.user_name(),
                email=fake.email(),
                password=generate_password_hash('password').decode('utf-8'),
                role='employer'
            )

            applicants.append(applicant)
    db.session.add_all(applicants)
    db.session.commit()

    #Seed Jobs
    jobs = []
    for _ in range(10):
        job = Job(
                title=fake.job(),
                description=fake.text(),
                company=fake.company(),
                location=fake.city(),
                employer_id=fake.random_element(elements=[user.id for user in users if user.role == 'employer'])
            )
        
        jobs.append(job)
        db.session.add_all(jobs)
        db.session.commit()  

    #Seed Applications
    applications=[]
    for _ in range(20):
        application = Application(
            user_id = fake.random_element(elements=[applicant.id for applicant in applicants ]),
            job_id = fake.random_element(elements=[job.id for job in jobs]),
            status = fake.random_element(elements=['Pending', 'Accepted', 'Rejected']),
            date_applied=fake.date_time_this_year(before_now=True, after_now=False)    
        )
        applications.append(application)

    db.session.add_all(applications)
    db.session.commit()

    print("Database seeded successfully!")

    if __name__ == '__main__':
        seed_data() 



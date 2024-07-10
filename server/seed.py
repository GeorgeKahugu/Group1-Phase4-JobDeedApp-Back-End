from models import User, db, Job, Application
from app import app
from datetime import datetime 
from faker import Faker

def seed_data():
    fake = Faker()

    with app.app_context():

    #Drop all tables and create them

        db.drop_all()
        db.create_all()
   
         # Seed Users
        users = []
        for _ in range(5):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=generate_password_hash('password').decode('utf-8'),
                role='employer'
            )
        
        users.append(user)
    db.session.add_all(users)
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


          
        
        
        

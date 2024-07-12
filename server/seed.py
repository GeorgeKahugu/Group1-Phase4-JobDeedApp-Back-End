from faker import Faker
from sqlalchemy import func
from app import app
from models import db, Applicant, Job, Application

with app.app_context():
    fake=Faker()

    #Delete all records/rows in the applicants table
    Applicant.query.delete()

    #Empty list of applicants
    applicants = []

    roles = ['Software Developer', 'DevOps Engineer', 'Accountant', 'DataScientist', 'UX/UI Designer']

    for _ in range(50):
        username=fake.user_name()
        domain=fake.free_email_domain()
        email=f"{username}@{domain}"
        password=fake.password()
        role= fake.random.choice(roles)
        
    
        applicants.append(Applicant(username=username, email=email, password=password, role=role))


    
    db.session.add_all(applicants)
    db.session.commit()


    # Delete all records/rows in the jobs table
    Job.query.delete()

     
    #Empty list of jobs
    jobs = []

    job_titles = [ 'Junior Software Developer', 'Senior Software Developer', 'DevOps Specialist', 'Senior Accountant',
        'Junior Accountant', 'Data Analyst', 'Data Scientist', 'UX Designer', 'UI Designer'
    ]

    for _ in range(50):
        title = fake.random.choice(job_titles)
        description=fake.text()
        company= fake.company()
        location = fake.city()
        employer_id = fake.uuid4()
        print(employer_id)

        jobs.append(Job(title=title, description=description, company=company, location=location, employer_id=employer_id))

    db.session.add_all(jobs)
    db.session.commit()
    

    #Delete all applications in the applications table
    Application.query.delete()

    #Empty List of Applications
    applications = []

    #Generate applications
    for _ in range(50):

        # Select a random applicant and job
        applicant = Applicant.query.order_by(func.random()).first()
        job = Job.query.order_by(func.random()).first()

        status = fake.random.choice(['Pending', 'Accepted', 'Rejected'])
        date_applied= fake.date_time_between(start_date='-1y', end_date='now')

        applications.append(Application(
            applicant_id=applicant.id,
            job_id=job.id,
            status=status,
            date_applied=date_applied
        ))

    #Add all applications to the session and commit
    db.session.add_all(applications)
    db.session.commit()

    print("Data seeding for applications completed.")





from faker import Faker
from app import app
from models import db, Applicant, Job

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


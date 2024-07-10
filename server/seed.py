from models import db, Applicant, Job, Application
from app import app
from datetime import datetime 
from faker import Faker

def seed_data():
    fake = Faker()

    with app.app_context():

    #Drop all tables and create them

        db.drop_all()
        db.create_all()
    #Seed Users
    
          
        
        
        

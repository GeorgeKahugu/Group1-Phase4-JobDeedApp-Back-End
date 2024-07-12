from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS


from models import db, Applicant     

# Job, Application

#Initialize the Flask Application
app = Flask(__name__)

#Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)

migrate= Migrate(app, db)
db.init_app(app)





if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


# from flask import Flask,  request, jsonify
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS


# from models import db, Applicant, Job, Application


# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS(app)

# migrate= Migrate(app, db)
# db.init_app(app)



# # Routes
# @app.route('/')
# def index():
#     return 'Welcome To The Job Portal!!!'

# #crud <create the jobs>
# @app.route('/jobs')
# def list_jobs():
#     jobs = Job.query.all()
#     return jsonify('list_jobs.html', jobs=jobs)

# @app.route('/jobs/create', methods=['GET', 'POST'])
# def create_job():
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         company = request.form['company']
#         location = request.form['location']
#         employer_id = request.form['employer_id']


#         new_job = Job(title=title, description=description, company=company, location=location, employer_id=employer_id)
#         db.session.add(new_job)
#         db.session.commit()
#         return jsonify('index')
    
  

# #delete jobs
# @app.route('/jobs/<int:job_id>/delete', methods=['POST'])
# def delete_job(job_id):
#     job = Job.query.get_or_404(job_id)
#     db.session.delete(job)
#     db.session.commit()
#     return jsonify('list_jobs')

# #update jobs
# @app.route('/jobs/<int:job_id>/update', methods=['GET', 'POST'])
# def update_job(job_id):
#     job = Job.query.get_or_404(job_id)
#     if request.method == 'POST':
#         job.title = request.form['title']
#         job.description = request.form['description']
#         job.company = request.form['company']
#         job.location = request.form['location']
#         job.employer_id = request.form['employer_id']
        
#         db.session.commit()
#         return jsonify('list_jobs')
   

# #applicants
# @app.route('/applicants/create', methods=['GET', 'POST'])
# def create_applicant():
#     if request.method == 'POST':
#         name = request.json.get('username')
#         email = request.json.get('email')
#         password = request.json.get('password')
#         role = request.json.get('role')
        
#         new_applicant = Applicant(username=name, email=email, password=password, role=role)
#         db.session.add(new_applicant)
#         db.session.commit()
#         return jsonify(new_applicant)
   


# @app.route('/applicants/<int:applicant_id>/update', methods=['GET', 'POST'])
# def update_applicant(applicant_id):
#     applicant = Applicant.query.get_or_404(applicant_id)
#     if request.method == 'POST':    
#         applicant.name = request.form['name']
#         applicant.email = request.form['email']
#         applicant.password = request.form['password']
#         applicant.role = request.form['role']
        
#         db.session.commit()
#         return jsonify('list_applicants')
   

# # Delete applicants
# @app.route('/applicants/<int:applicant_id>/delete', methods=['POST'])
# def delete_applicant(applicant_id):
#     applicant = Applicant.query.get_or_404(applicant_id)
#     db.session.delete(applicant)
#     db.session.commit()
#     return jsonify('list_applicants')

# #application
# #create
# @app.route('/applicantion/create', methods=['GET', 'POST'])
# def create_application():
#     if request.method == 'POST':
#         user = request.form['user']
#         status = request.form['status']
#         role = request.form['role']
#         new_application = Application(user=user, status=status, role=role)
#         db.session.add(new_application)
#         db.session.commit()
#         return jsonify('index')
    
   
# #delete applications
# @app.route('/application/<int:application_id>/delete', methods=['POST'])
# def delete_application(application):
#     job = Job.query.get_or_404(application)
#     db.session.delete(application)
#     db.session.commit()
#     return jsonify('list_application')

# # Routes
# @app.route('/')
# def index():
#     return 'Welcome To The Job Portal!!!'

# # List jobs
# @app.route('/jobs')
# def list_jobs():
#     jobs = Job.query.all()
#     jobs_data = [{'id': job.id, 'title': job.title, 'description': job.description, 'company': job.company, 'location': job.location, 'employer_id': job.employer_id} for job in jobs]
#     return jsonify(jobs=jobs_data)

# # Create job
# @app.route('/jobs/create', methods=['POST'])
# def create_job():
#     data = request.json
#     new_job = Job(
#         title=data['title'],
#         description=data['description'],
#         company=data['company'],
#         location=data['location'],
#         employer_id=data['employer_id']
#     )
#     db.session.add(new_job)
#     db.session.commit()
#     return jsonify(job={'id': new_job.id, 'title': new_job.title, 'description': new_job.description, 'company': new_job.company, 'location': new_job.location, 'employer_id': new_job.employer_id})

# # Delete job
# @app.route('/jobs/<int:job_id>/delete', methods=['POST'])
# def delete_job(job_id):
#     job = Job.query.get_or_404(job_id)
#     db.session.delete(job)
#     db.session.commit()
#     return jsonify({'message': 'Job deleted successfully'})

# # Update job
# @app.route('/jobs/<int:job_id>/update', methods=['POST'])
# def update_job(job_id):
#     job = Job.query.get_or_404(job_id)
#     data = request.json
#     job.title = data['title']
#     job.description = data['description']
#     job.company = data['company']
#     job.location = data['location']
#     job.employer_id = data['employer_id']
#     db.session.commit()
#     return jsonify(job={'id': job.id, 'title': job.title, 'description': job.description, 'company': job.company, 'location': job.location, 'employer_id': job.employer_id})

# # Create applicant
# @app.route('/applicants/create', methods=['POST'])
# def create_applicant():
#     data = request.json
#     new_applicant = Applicant(
#         name=data['name'],
#         email=data['email'],
#         password=data['password'],
#         role=data['role']
#     )
#     db.session.add(new_applicant)
#     db.session.commit()
#     return jsonify(applicant={'id': new_applicant.id, 'name': new_applicant.name, 'email': new_applicant.email, 'role': new_applicant.role})

# # Update applicant
# @app.route('/applicants/<int:applicant_id>/update', methods=['POST'])
# def update_applicant(applicant_id):
#     applicant = Applicant.query.get_or_404(applicant_id)
#     data = request.json
#     applicant.name = data['name']
#     applicant.email = data['email']
#     applicant.password = data['password']
#     applicant.role = data['role']
#     db.session.commit()
#     return jsonify(applicant={'id': applicant.id, 'name': applicant.name, 'email': applicant.email, 'role': applicant.role})

# # Delete applicant
# @app.route('/applicants/<int:applicant_id>/delete', methods=['POST'])
# def delete_applicant(applicant_id):
#     applicant = Applicant.query.get_or_404(applicant_id)
#     db.session.delete(applicant)
#     db.session.commit()
#     return jsonify({'message': 'Applicant deleted successfully'})

# # Create application
# @app.route('/application/create', methods=['POST'])
# def create_application():
#     data = request.json
#     new_application = Application(
#         user=data['user'],
#         status=data['status'],
#         role=data['role']
#     )
#     db.session.add(new_application)
#     db.session.commit()
#     return jsonify(application={'id': new_application.id, 'user': new_application.user, 'status': new_application.status, 'role': new_application.role})

# # Delete application
# @app.route('/application/<int:application_id>/delete', methods=['POST'])
# def delete_application(application_id):
#     application = Application.query.get_or_404(application_id)
#     db.session.delete(application)
#     db.session.commit()
#     return jsonify({'message': 'Application deleted successfully'})
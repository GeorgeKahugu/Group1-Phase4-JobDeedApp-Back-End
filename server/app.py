from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import Applicant, Job, Application


from flask import Flask


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    return 'Welcome to the job portal!'

#crud <create the jobs>
@app.route('/jobs')
def list_jobs():
    jobs = Job.query.all()
    return render_template('list_jobs.html', jobs=jobs)

@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']
        employer_id = request.form['employer_id']


        new_job = Job(title=title, description=description, company=company, location=location, employer_id=employer_id)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('create_job.html')

#delete jobs
@app.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('list_jobs'))

#update jobs
@app.route('/jobs/<int:job_id>/update', methods=['GET', 'POST'])
def update_job(job_id):
    job = Job.query.get_or_404(job_id)
    if request.method == 'POST':
        job.title = request.form['title']
        job.description = request.form['description']
        job.company = request.form['company']
        job.location = request.form['location']
        job.employer_id = request.form['employer_id']
        
        db.session.commit()
        return redirect(url_for('list_jobs'))
    return render_template('update_job.html', job=job)

#applicants
@app.route('/applicants/create', methods=['GET', 'POST'])
def create_applicant():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        new_applicant = Applicant(name=name, email=email, password=password, role=role)
        db.session.add(new_applicant)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_applicant.html')


@app.route('/applicants/<int:applicant_id>/update', methods=['GET', 'POST'])
def update_applicant(applicant_id):
    applicant = Applicant.query.get_or_404(applicant_id)
    if request.method == 'POST':
        applicant.name = request.form['name']
        applicant.email = request.form['email']
        applicant.password = request.form['password']
        applicant.role = request.form['role']
        
        db.session.commit()
        return redirect(url_for('list_applicants'))
    return render_template('update_applicant.html', applicant=applicant)

# Delete applicants
@app.route('/applicants/<int:applicant_id>/delete', methods=['POST'])
def delete_applicant(applicant_id):
    applicant = Applicant.query.get_or_404(applicant_id)
    db.session.delete(applicant)
    db.session.commit()
    return redirect(url_for('list_applicants'))

#application
#create
@app.route('/applicantion/create', methods=['GET', 'POST'])
def create_application():
    if request.method == 'POST':
        user = request.form['user']
        status = request.form['status']
        role = request.form['role']
        new_application = Application(user=user, status=status, role=role)
        db.session.add(new_application)
        db.session.commit()
        return redirect(url_for('index'))
    

    return render_template('create_application.html') 
    
#delete applications
@app.route('/application/<int:application_id>/delete', methods=['POST'])
def delete_application(application):
    job = Job.query.get_or_404(application)
    db.session.delete(application)
    db.session.commit()
    return redirect(url_for('list_application'))

if __name__ == '__main__':
    app.run(debug=True, port=5555)
    

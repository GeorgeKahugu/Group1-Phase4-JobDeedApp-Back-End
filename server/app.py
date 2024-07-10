from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
@app.route('/jobs/create', methods=['GET', 'POST'])
def create_job():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        company = request.form['company']
        location = request.form['location']
        employer_id = request.form['employer_id']


        new_job = JOB(title=title, description=description, company=company, location=location, employer_id=employer_id)
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

if __name__ == '__main__':
    app.run(debug=True, port=5555)
    

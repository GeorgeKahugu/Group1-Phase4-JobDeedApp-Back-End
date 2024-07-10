from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_portal.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Routes
@app.route('/')
def index():
    return 'Welcome to the job portal!'

# CRUD operations 


if __name__ == '__main__':
    app.run(debug=True, port=5555)
    

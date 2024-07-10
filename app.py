from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Helo world!</h1>'

@app.route('/jobs')
def user():
    return '<h1>Here are the jobs for the apllicants.</h1>'

@app.route('/user')
def index ():
    return "job applications"

if __name__ == '__main__':
    app.run(port=5555, debug=True)
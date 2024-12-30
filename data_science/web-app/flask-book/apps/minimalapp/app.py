from flask import Flask, render_template, url_for, current_app, g

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, Flaskbook!"

@app.route('/hello/<name>',
           methods = ["GET"],
           endpoint = "hello-endpoint",)
def hello(name):
    return f"Hello, {name}!"

@app.route('/name/<name>')
def show_name(name):
    return render_template('index.html', name=name)

with app.test_request_context():

    print(url_for('index'))

    print(url_for('hello-endpoint', name='world'))
          
    print(url_for('show_name', name='ichiro', page='1'))
    print(url_for('static', filename='style.css'))
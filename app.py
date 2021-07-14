from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/greeting')
def my_greeting():
    return = 'Welcome back to the ACEER training.'


if __name__ == '__main__':
    app.run()
from flask import Flask,jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/greeting')
def my_greeting():
    return jsonify(message='Welcome back to the ACEER training.')


if __name__ == '__main__':
    app.run()
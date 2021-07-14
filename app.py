from flask import Flask,jsonify


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/greeting')
def my_greeting():
    return jsonify(message='Welcome back to the ACEER training.'), 200

@app.route('/not_found')
def not_found():
    return jsonify(message='That resource was not found'), 404


if __name__ == '__main__':
    app.run()
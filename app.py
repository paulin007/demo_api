from flask import Flask,jsonify, request


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


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 21:
        return jsonify(message="Sorry " + name + ", you are not old enough to subscribe to our term deposit"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are eligible to our term deposit", amout=100)


@app.route('/parameters_modern/<string:name>/<int:age>')
def parameters_modern(name: str, age: int):
    if age < 21:
        return jsonify(message="Sorry " + name + ", you are not old enough to subscribe to our term deposit"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are eligible to our term deposit", amout=100)


if __name__ == '__main__':
    app.run()
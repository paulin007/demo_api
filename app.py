from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI should be name exactly like otherwise it not going to work
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bank.db')


db = SQLAlchemy(app)


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


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Account(db.Model):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    job = Column(String) #  type of job (categorical: 'admin.','blue-collar','entrepreneur','housemaid','management','retired','self-employed','services','student','technician','unemployed','unknown')
    marital = Column(String) # marital status (categorical: 'divorced','married','single','unknown'; note: 'divorced' means divorced or widowed)
    education = Column(String) # (categorical: 'basic.4y','basic.6y','basic.9y','high.school','illiterate','professional.course','university.degree','unknown')
    default = Column(String) # has credit in default? (categorical: 'no','yes','unknown')
    housing = Column(String) # has housing loan? (categorical: 'no','yes','unknown')
    loan = Column(String) # has personal loan? (categorical: 'no','yes','unknown')
    balance = Column(Float)
    part_of_training = Column(Boolean)

class TermDepositPrediction(db.Model):
    __tablename__ = 'Predictions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    model_name = Column(String) # term deposit predition
    model_version = Column(String) # v0.1
    pred_eligible_term_deposit = Column(Boolean)
    inference_date = Column(Date)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


@app.cli.command('db_seed')
def db_seed():
    account_1 = Account(age= 18,
                     job='entrepreneur',
                     marital='single',
                     education='university.degree',
                     default='yes',
                     housing='no',
                     loan='unknown',
                     balance=1516,
                     part_of_training=True)

    account_2 = Account(age= 78,
                     job='retired',
                     marital='divorced',
                     education='unknown',
                     default='no',
                     housing='yes',
                     loan='yes',
                     balance=6516,
                     part_of_training=True)

    db.session.add(account_1)
    db.session.add(account_2)


    paulin_user = User(first_name='Paulin',
                     last_name='T',
                     email='paulin@test.com',
                     password='P@ssw0rd')

    db.session.add(paulin_user)
    db.session.commit()
    print('Database seeded!')


if __name__ == '__main__':
    app.run()
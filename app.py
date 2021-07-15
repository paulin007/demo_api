from flask import Flask,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import config as cg
import datetime
import sys

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI should be name exactly like otherwise it not going to work
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bank.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'  # change this

db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

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


@app.route('/accounts', methods=['GET'])
def accounts():
    accounts_list = Account.query.all()
    #return jsonify(data=accounts_list)
    result = accounts_schema.dump(accounts_list) # serialize results
    return jsonify(result)

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists.'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User created successfully."), 201

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email) # identity is how we want to identify our user
        return jsonify(message="Login succeeded!", access_token=access_token)
    else:
        return jsonify(message="Bad email or password"), 401

@app.route('/account_details/<int:account_id>', methods=["GET"])
def account_details(account_id: int):
    account = Account.query.filter_by(id=account_id).first()
    if account:
        result = account_schema.dump(account) # serialization single version
        return jsonify(result)
    else:
        return jsonify(message="That account does not exist"), 404

@app.route('/add_account', methods=['POST'])
@jwt_required()
def add_account():
    try:
        app.logger.info("adding a new account data..")
        account_id = int(request.form['account_id'])
        test = Account.query.filter_by(id=account_id).first()
        if test:
            return jsonify("There is already a account with that id"), 409
        else:
            age = int(request.form['age'])
            job = request.form['job']
            marital = request.form['marital']
            education = request.form['education']
            default = request.form['default']
            housing = request.form['housing']
            loan = request.form['loan']
            balance = float(request.form['balance'])
            pred_eligible_term_deposit = bool(request.form['pred_eligible_term_deposit'])
            
            if job not in cg.CAT_job:
                return jsonify(message="Job '"+job+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_job) ), 400
            if marital not in cg.CAT_marital:
                return jsonify(message="marital '"+marital+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_marital) ), 400
            if education not in cg.CAT_education:
                return jsonify(message="education '"+marital+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_education) ), 400
            if default not in cg.CAT_BOOL_unknown:
                return jsonify(message="default '"+marital+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_BOOL_unknown) ), 400
            if housing not in cg.CAT_BOOL_unknown:
                return jsonify(message="housing '"+marital+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_BOOL_unknown) ), 400
            if loan not in cg.CAT_BOOL_unknown:
                return jsonify(message="loan '"+marital+"'"+" is incorrect.. Should be: "+",".join(cg.CAT_BOOL_unknown) ), 400

            new_account = Account(id=account_id,
                                age=age,
                                job=job,
                                marital=marital,
                                education=education,
                                default=default,
                                housing=housing,
                                loan=loan,
                                balance=balance,
                                pred_eligible_term_deposit = pred_eligible_term_deposit,
                                part_of_training=False)

            db.session.add(new_account)
            db.session.commit()
    except BaseException as ex:
        import traceback
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()
        app.logger.error(ex)
        for trace in trace_back:
            stack_trace.append("File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))
        
        my_error = ErrorAPI()
        my_error.errorType = "-"
        my_error.errorMsg=str(ex)+"  "+str(stack_trace)
        if request.remote_addr != None:
            my_error.ipAddress = request.remote_addr
        db.session.add(my_error)
        db.session.commit()
        
        return send_critical_msg(str(ex)+"  "+str(stack_trace))
    return jsonify(message="You added a account data"), 201

def send_error_msg(msg):
    app.logger.error(msg)
    return (jsonify({'status': 'error','msg':msg}), 400)

def send_critical_msg(msg):
    app.logger.critical(msg)
    return (jsonify({'status': 'error_on_server','msg':msg}), 500)

def send_success_msg(msg):
    app.logger.info(msg)
    return (jsonify({'status': 'success','msg':msg}), 200)


@app.route('/update_ground_truth', methods=['PUT'])
@jwt_required()
def update_ground_truth():
    app.logger.info("adding a new account data..")
    account_id = int(request.form['account_id'])
    account = Account.query.filter_by(id=account_id).first()
    if account:
        account.pred_eligible_term_deposit = bool(request.form['pred_eligible_term_deposit'])
        db.session.commit()
        return jsonify(message="You ground_truth have been updated successfully"), 202
    else:
        return jsonify("The account doesn't exist"), 404

@app.route('/remove_account/<int:account_id>', methods=['DELETE'])
@jwt_required()
def remove_account(account_id: int):
    account = Account.query.filter_by(id=account_id).first()
    if account:
        db.session.delete(account)
        db.session.commit()
        return jsonify(message="You deleted a Account"), 202
    else:
        return jsonify(message="That Account does not exist"), 404

# database models

class ErrorAPI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    errorType = db.Column(db.String(255), index=False, unique=False, nullable=True)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=True,
        default=datetime.datetime.now()
    )
    errorMsg = db.Column(db.Text, index=False, unique=False, nullable=True)

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
    pred_eligible_term_deposit = Column(Boolean) # grouth true
    part_of_training = Column(Boolean)

class TermDepositPrediction(db.Model):
    __tablename__ = 'Predictions'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    model_name = Column(String) # term deposit predition
    model_version = Column(String) # v0.1
    pred_eligible_term_deposit = Column(Boolean)
    inference_date = Column(Date)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id', 'age', 'job', 'marital', 'education', 'default', 'housing', 'loan', 'balance')

class TermDepositPredictionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'account_id', 'model_name', 'model_version', 'pred_eligible_term_deposit', 'inference_date')

# instantiate two different copies of each schema
# give ability to serialize one single or multiple objects
user_schema = UserSchema()
users_schema = UserSchema(many=True) # plurial 

account_schema = AccountSchema()
accounts_schema = AccountSchema(many=True)

prediction_schema = TermDepositPredictionSchema()
predictions_schema = TermDepositPredictionSchema(many=True)

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
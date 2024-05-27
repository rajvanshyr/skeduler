from flask import Flask, render_template, request, jsonify
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://u21vm5h75knqle:p449e4facb4556152409922cbd0a26ca356b593e7336dd9e60bf72de4b051e1eb@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1sqbtf1qlslff'
#connect to postgres db 
#DATABASE_URL: postgres://u21vm5h75knqle:p449e4facb4556152409922cbd0a26ca356b593e7336dd9e60bf72de4b051e1eb@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1sqbtf1qlslff

db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Log_on'
app.secret_key = "app secret key"

class User(UserMixin, db.Model):
	__tablename__='User'
	userid = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
	username=db.Column(db.String(250),primary_key=True)
	password=db.Column(db.String(250))
	email=db.Column(db.String(250))
	firstname=db.Column(db.String(250))
	lastname=db.Column(db.String(250))
	credit_numbers=db.Column(db.Integer())
	account_created=db.Column(db.String(250))
 
	def __init__(self,username,password,email,firstname,lastname,credit_numbers,account_created):
		self.username=username
		self.password=password
		self.email=email
		self.firstname=firstname
		self.lastname=lastname
		self.credit_numbers=credit_numbers
		self.account_created=account_created
	
	def get_id(self):
		return self.username
	
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

@app.route("/")
def hello_world():
	return render_template('home.html')

@app.route("/profile")
@login_required
def Profile():
	return render_template('profile.html', user = current_user)

@app.route("/Log-on")
def Log_on():
	return render_template('signin.html')

@app.route("/Sign-on")
def Sign_on():
	return render_template('signin.html')

@app.route('/Log-out')
@login_required
def logout():
    logout_user()
    return render_template('home.html')
	
@app.route("/api/registration", methods=['POST'])
def registration():
	data = request.get_json()
	username = data.get('username', None)
	password = data.get('password', None)
	firstname = data.get('firstname', None)
	lastname = data.get('lastname', None)
	email = data.get('email', None)
	credit_numbers = data.get('credit_numbers',None)
	account_created = date.today()
	try:
		user=db.session.query(User).filter(User.username==username).first()
		if user:
			raise Exception("Username already exists.")
		else:
			user=User(username=username,password=password,email=email,firstname=firstname,
				account_created=account_created,lastname=lastname,credit_numbers=credit_numbers)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return jsonify({"message": "User Created"}), 201
	except Exception as error:
		return jsonify({"error": f"{error}"}), 400
	
@app.route("/api/login", methods=['POST'])
def login():
	data = request.get_json()
	username = data.get('username', None)
	password = data.get('password', None)
	try:
		user=db.session.query(User).filter(User.username==username, User.password==password).first()
		if user:
			login_user(user)
			return jsonify({"message": "Logged in successfully"}), 200
		else:
			raise Exception("Invalid credentials")
	except Exception as error:
		return jsonify({"error": f"{error}"}), 400
		 

if __name__ == "__main__":
	app.run(host='0.0.0.0')

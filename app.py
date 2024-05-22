from flask import Flask
app = Flask(__name__)

#connect to postgres db 
#DATABASE_URL: postgres://u21vm5h75knqle:p449e4facb4556152409922cbd0a26ca356b593e7336dd9e60bf72de4b051e1eb@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1sqbtf1qlslff


@app.route("/")
def hello_world():
	return "<h1 style='color:green'>Home Page!!</h1>"


#Behind authentication
@app.route("/profile")
def Profile():
	 return 'Profile'

@app.route("/Log-on")
def Log_on():
	 return 'Log-on'

@app.route("/Sign-on")
def Sign_on():
	 return 'Sign-on'	 

if __name__ == "__main__":
	app.run(host='0.0.0.0')

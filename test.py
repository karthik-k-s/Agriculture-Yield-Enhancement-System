from flask import Flask,render_template,redirect,flash,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from Forms import LoginForm, RegistrationForm
from flask_mysqldb import MySQL
import requests

app = Flask(__name__)
app.config['SECRET_KEY']="Alohomora"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Alohomora'
app.config['MYSQL_DB'] = 'agriculture'

mysql = MySQL(app)
Bootstrap(app)


#post=[{'a':'1'},{'a':'2'},{'a':'3'},{'a':'4'},{'a':'5'},{'a':'6'},{'a':'7'},{'a':'8'},{'a':'9'}]

@app.route('/', methods=['GET', 'POST'])
def first_page():
	return render_template("firstpage.html")

@app.route('/login', methods=['POST','GET'])
def login():
	form=LoginForm()
	print(form.errors)
	print("1")
	cur = mysql.connection.cursor()
	print("2")
	if form.validate_on_submit():
		print("3")
		print("COMING HERE")
	print("4")
	return render_template("loginold.html", form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
	form=RegistrationForm()
	return render_template("register.html",form=form)

if __name__=="__main__":
	app.run(debug=True)
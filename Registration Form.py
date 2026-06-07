# IMPORTING 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

#INTERACTION
web = Flask(__name__)
web.config['SECRET_KEY'] = 'secret123'
web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
web.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(web)

#Create Database Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    password = db.Column(db.String(100))

#Create Registration Form Using FLASK-WTF FORM
class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    emailid = StringField("Email", validators=[DataRequired(), Email()])
    phonenumber = StringField("Phone Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmpassword = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password')]
    )

#MAPPING
@web.route('/', methods=['GET','POST'])
@web.route('/register', methods=['GET','POST'])

#INPUTS
def homepage():
    form = RegisterForm()

    if form.validate_on_submit():

        n = form.name.data
        e = form.emailid.data
        p = form.phonenumber.data
        pwd = form.password.data
        
        # SAVE DATA IN DATABASE
        user = User(name=n, email=e, phone=p, password=pwd)
        db.session.add(user)
        db.session.commit()

        return render_template('confirm.html', name = n, emailid = e, phonenumber = p)
    return render_template('register.html', form=form)

@web.route("/users")
def show_users():
    users = User.query.all()

    output = ""
    for u in users:
        output += f"{u.name} - {u.email} - {u.phone}<br>"

    return output

# MAIN
if __name__ == "__main__":
    with web.app_context():
        db.create_all()

    web.run(debug=True)
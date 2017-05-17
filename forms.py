from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, BooleanField
from wtforms.validators import Email, InputRequired, DataRequired, Length, Optional


class ApplicantForm(FlaskForm):
	fname = StringField('First Name', validators=[InputRequired(), DataRequired()])
	lname = StringField('Last Name', validators=[InputRequired(), DataRequired()])
	email = StringField('Email', validators=[Email(), InputRequired(), DataRequired()])
	age = IntegerField('Age', validators=[InputRequired()])
	city = StringField('City', validators=[InputRequired(), DataRequired()])
	state = StringField('State', validators=[InputRequired(), DataRequired()])
	zip_code = StringField('Zip Code', validators=[InputRequired(), DataRequired()])
	phone_number = StringField('Phone Number', validators=[InputRequired(), DataRequired()])
	password = PasswordField('Password', validators=[InputRequired(), DataRequired(), Length(min=8, max=27)])
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Email(), InputRequired()])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=27)])
	submit = SubmitField('Login')

class EditForm(FlaskForm):
	fname = StringField('First Name', validators=[Optional()])
	lname = StringField('Last Name', validators=[Optional()])
	email = StringField('Email', validators=[Email(), Optional()])
	age = IntegerField('Age', validators=[Optional()])
	city = StringField('City', validators=[Optional()])
	state = StringField('State', validators=[Optional()])
	zip_code = StringField('Zip Code', validators=[Optional()])
	phone_number = StringField('Phone Number', validators=[Optional()])
	submit = SubmitField('Submit Edits')
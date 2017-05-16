from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import Email, InputRequired, DataRequired, Length


class ApplicantForm(FlaskForm):
	fname = StringField('First Name', validators=[InputRequired(), DataRequired()])
	lname = StringField('Last Name', validators=[InputRequired(), DataRequired()])
	email = StringField('Email', validators=[Email(), InputRequired(), DataRequired()])
	age = IntegerField('Age', validators=[InputRequired(), DataRequired()])
	city = StringField('City', validators=[InputRequired(), DataRequired()])
	state = StringField('State', validators=[InputRequired(), DataRequired()])
	zip_code = StringField('Zip Code' validators=[InputRequired(), DataRequired()])
	phone_number = StringField('Phone Number' validators=[InputRequired(), DataRequired()])
	password = PasswordField('Password', validators=[InputRequired(), DataRequired(), Length(min=8, max=27)])
	submit = SubmitField('Submit')
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ApplicantForm(FlaskForm):
	fname = StringField('First Name', validators=[DataRequired(), Length(5,100)])
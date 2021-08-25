from Flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired,Length

class registration(FlaskForm):
	username=StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
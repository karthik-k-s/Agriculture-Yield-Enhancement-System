from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,FileField,SelectField
from wtforms.validators import DataRequired,Length, EqualTo,Email,regexp
from wtforms.fields.html5 import TelField
from wtforms import ValidationError
import phonenumbers



"""class Input(object):
    
    html_params = staticmethod(html_params)

    def __init__(self, input_type=None):
        if input_type is not None:
            self.input_type = input_type

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        return HTMLString('<input %s>' % self.html_params(name=field.name, **kwargs))
"""
"""class PasswordInput(Input):
   
    input_type = 'password'

    def __init__(self, hide_value=True):
        self.hide_value = hide_value

    def __call__(self, field, **kwargs):
        if self.hide_value:
            kwargs['value'] = ''
        return super(PasswordInput, self).__call__(field, **kwargs)"""



class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password= PasswordField("Password",validators=[DataRequired()])
    #submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    #phonenumber = IntegerField('Mobile Number',validators=[DataRequired(),Length(min=10, max=10)])
    name = StringField('Username',validators=[DataRequired()])
    mobileno = StringField('Mobile Number',validators=[DataRequired()])
    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
    lang = StringField('Language',validators=[DataRequired()])
    email = StringField('Email Address',validators=[Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #submit = SubmitField('Submit')

class CropForm(FlaskForm):
    cname = StringField('Crop Name',validators=[DataRequired()])
    nit = StringField('Nitrogen',validators=[DataRequired()])
    phos = StringField('Phosphorous',validators=[DataRequired()])
    pot = StringField('Potassium',validators=[DataRequired()])

class DeleteCrop(FlaskForm):
    name = StringField('Crop Name',validators=[DataRequired()])

class DeleteUser(FlaskForm):
    uname = StringField('User Name',validators=[DataRequired()])

class ForgotPass(FlaskForm):
    email = StringField('Email Address',validators=[Email()])


class UploadForm(FlaskForm):
    size = StringField('Land Size',validators=[DataRequired()])

class FeedbackForm(FlaskForm):
    fd = StringField('Feedback',validators=[DataRequired()])

class RegionForm(FlaskForm):
        region =SelectField('Region',choices=[('1','Bangalore (U)'),('2','Bangalore (R)'),('3','Kolar'),('4','Tumkur'),('5','Shimoga'),('6','Chitradurga'),('7','Davanagere'),('8','Mysore'),('9','Chamarajanagar'),('10','Mandya')])
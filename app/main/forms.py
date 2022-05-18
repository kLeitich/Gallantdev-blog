from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,ValidationError,BooleanField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    username = StringField('Enter your username',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators =[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')


class NewBlog(FlaskForm):
    category = SelectField(u'Categories', choices=[('Tech Blog','Tech Blog'), ('Story Blog','Story Blog'), ('Articles','Articles'), ('Personal story','Personal Story')])
    blogTitle=StringField('Title of you blog',validators=[DataRequired()])
    blogContent = TextAreaField('Write your blog here.',validators = [DataRequired()])
    submit = SubmitField('Submit')

class NewComment(FlaskForm):
    commentNew = TextAreaField('Please Add a Comment',validators = [DataRequired()])
    submit = SubmitField('Submit')

class EmailSubscription(FlaskForm):
    email = StringField('Your Email Address',validators=[DataRequired(),Email()])
    submit = SubmitField('Subscribe')
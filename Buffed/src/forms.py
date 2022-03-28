from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf


class ContactForm(FlaskForm):
    name = StringField("Name")
    email = EmailField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")
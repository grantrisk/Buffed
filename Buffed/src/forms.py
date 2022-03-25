from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


class ContactForm(FlaskForm):
    """
    Creates contact form with validation specifications
    """
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")

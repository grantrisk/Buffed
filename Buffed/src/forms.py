import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField, DateField, DecimalField, \
    RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Regexp, NumberRange, Length



class MultiCheckboxField(SelectMultipleField):
    """
    Checkbox version of multiselect field
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    More on this: https://wtforms.readthedocs.io/en/3.0.x/specific_problems/#specialty-field-tricks
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ContactForm(FlaskForm):
    """
    Creates contact form with validation specifications and alert details
    """
    # flag for alerting users if the form doesn't work
    available = False
    alert = 'warning'  # alert category, for bootstrap formatting
    alert_msg = "Sorry, our contact form is not ready to use yet!"

    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


#
# def validate_birth(form,field):
#     if (datetime.date.today().year - int(field.data[:4])) < (13 * 365):
#         raise ValidationError("You must be 13 years or older!")


class ProfileQuestionnaire(FlaskForm):
    """
    Form for profile questionnaire
    """
    # Personal Questionnaire
    # optional: adjust validation/error messages for bday and height
    name = StringField("Display Name", [DataRequired(),
                                        Length(min=1, max=16, message='Must be between 1-16 characters long')])
    sex = RadioField("Sex", [DataRequired()], choices=["Male", "Female"])
    birth = DateField("Birthdate", [DataRequired()])
    weight = DecimalField("Weight (lb)", [DataRequired(),
                                          NumberRange(min=0, max=5000, message='Must be a number between 0-5000.')])
    height = StringField('Height (Feet-Inch)', [DataRequired(),
                                                Regexp('[2-9]\'[0-9]', message='Wrong height format. Example: 6\'0')])
    activity = RadioField("Activity Level", [DataRequired()], choices=["Very Active", "Moderately Active",
                                                                           "Lightly Active", "Sedentary"])

    # Diet Information: Based on Health Labels
    diet_type = MultiCheckboxField("Diet Type",
                                   choices=['Vegan', 'Vegetarian', 'Pescatarian', 'Dairy-Free',
                                            'Gluten-Free', 'Wheat-Free', 'Egg-Free', 'Peanut-Free',
                                            'Tree-Nut-Free', 'Soy-Free', 'Fish-Free', 'Shellfish-Free',
                                            'Pork-Free', 'Red-Meat-Free', 'Crustacean-Free', 'Celery-Free',
                                            'Mustard-Free', 'Sesame-Free', 'Lupine-Free', 'Mollusk-Free',
                                            'Alcohol-Free', 'No oil added', 'FODMAP-Free', 'Kosher'])

    submit = SubmitField("Save")
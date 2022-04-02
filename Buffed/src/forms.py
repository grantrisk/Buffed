from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, SelectField, DateField, DecimalField, \
    RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Email

from Buffed.src.models import Goal


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


class ProfileQuestionnaire(FlaskForm):
    """
    Form for profile questionnaire
    """
    # what does sex/gender do for us? do we care for calories?
    sex = SelectField("Sex", [DataRequired()], choices=["Male", "Female", "Other"])
    bday = DateField("Birthdate", [DataRequired()])
    weight = DecimalField("Weight in", [DataRequired()])
    height = DecimalField("Height", [DataRequired()])
    activity_lvl = RadioField("Activity Level", [DataRequired()], choices=["Athletic", "Moderate", "Sedentary"])
    # TODO: ensure I'm using Goal object correctly; how to best update goal in user db?
    goal = Goal("0", "Default Goal", True, 1300, {'protein': 100, 'carbs': 140, 'fat': 100}, 3, 110)

    submit = SubmitField("Save")


class DietQuestionnaire(FlaskForm):
    """
    Form for diet questionnaire
    """
    # TODO: This is a draft; need to check Edamam what categories return; add food keyword search?
    diet_type = SelectMultipleField("Diet Type", [DataRequired()],
                                    choices=["Vegan", "Vegetarian", "Mediterranean",
                                             "Pescatarian", "Kosher", "Gluten-free",
                                             "Ketogenic", "Diabetic", "Other", "None"])

    allergies = SelectMultipleField("Allergies", [DataRequired()],
                                    choices=["Peanuts", "Nut oils", "Tree nuts", "Wheat",
                                             "Soybean/Soy", "Milk/Dairy", "Egg",
                                             "Fish", "Shellfish", "Sesame", "Potato",
                                             "Chocolate / Cacao", "Other", "None"])

    submit = SubmitField("Save")

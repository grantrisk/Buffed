from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField, DateField, DecimalField, \
    RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Regexp

from Buffed.src.models import Goal


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


class ProfileQuestionnaire(FlaskForm):
    """
    Form for profile questionnaire
    """
    # Personal Questionnaire
    # TODO: need to fix validation for bday, weight, and height ; need to show error messages
    sex = RadioField("Sex", [DataRequired()], choices=["Male", "Female"])
    bday = DateField("Birthdate", [DataRequired()])
    weight = DecimalField("Weight (lb)", [DataRequired()])
    height = StringField('Height (ft)',
                         [DataRequired(), Regexp('[3-7]\'\d{1,2}', message='Wrong height format. Example: 5\'7')])
    activity_lvl = RadioField("Activity Level", [DataRequired()], choices=["Athletic", "Moderate", "Sedentary"])

    # Goal Information: Based on Goal model
    # goal = Goal("0", "Default Goal", True, 1300, {'protein': 100, 'carbs': 140, 'fat': 100}, 3, 110)

    # Diet Information: Based on Health Labels
    diet_type = MultiCheckboxField("Diet Type",
                                   choices=['Vegan', 'Vegetarian', 'Pescatarian', 'Dairy-Free',
                                            'Gluten-Free', 'Wheat-Free', 'Egg-Free', 'Peanut-Free',
                                            'Tree-Nut-Free', 'Soy-Free', 'Fish-Free', 'Shellfish-Free',
                                            'Pork-Free', 'Red-Meat-Free', 'Crustacean-Free', 'Celery-Free',
                                            'Mustard-Free', 'Sesame-Free', 'Lupine-Free', 'Mollusk-Free',
                                            'Alcohol-Free', 'No oil added', 'FODMAP-Free', 'Kosher'])

    submit = SubmitField("Save")

#
# class DietQuestionnaire(FlaskForm):
#     """
#     Form for diet questionnaire
#     """
#     # TODO: This is a draft; need to check Edamam what categories return; add food keyword search?
#     diet_type = MultiCheckboxField("Diet Type", [DataRequired()],
#                                    choices=['Vegan', 'Vegetarian', 'Pescatarian', 'Dairy-Free',
#                                             'Gluten-Free', 'Wheat-Free', 'Egg-Free', 'Peanut-Free',
#                                             'Tree-Nut-Free', 'Soy-Free', 'Fish-Free', 'Shellfish-Free',
#                                             'Pork-Free', 'Red-Meat-Free', 'Crustacean-Free', 'Celery-Free',
#                                             'Mustard-Free', 'Sesame-Free', 'Lupine-Free', 'Mollusk-Free',
#                                             'Alcohol-Free', 'No oil added', 'FODMAP-Free', 'Kosher'])
#
#     allergies = MultiCheckboxField("Allergies", [DataRequired()],
#                                    choices=["Peanuts", "Nut oils", "Tree nuts", "Wheat",
#                                             "Soybean/Soy", "Milk/Dairy", "Egg",
#                                             "Fish", "Shellfish", "Sesame", "Potato",
#                                             "Chocolate / Cacao", "Other", "None"])
#
#     submit = SubmitField("Save")
#
#
# class AccountSetupForm(FlaskForm):
#     """
#     Form that combines the profile and diet forms
#     """
#     # we can combine both forms into one for the account set up,
#     # while preserving their individual forms for future use
#     profile_q = wtforms.FormField(ProfileQuestionnaire)
#     diet_q = wtforms.FormField(DietQuestionnaire)

import re
import email_validator
from firebase_admin import auth
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField, DateField, \
    RadioField, SelectMultipleField, widgets, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, NumberRange, Length, EqualTo, ValidationError


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
    # display flag
    display = False
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
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class ConfirmForm(FlaskForm):
    confirm = BooleanField("Yes", validators=[DataRequired()])


class ForgotPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])


class RegisterForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(message="Please fill in this field"),
                                            Email(check_deliverability=True), Length(min=7, max=50),
                                            EqualTo(fieldname="confirm_email", message="Emails don't match.")])
    confirm_email = EmailField("Confirm Email", validators=[DataRequired(message="Please fill in this field"), Email(),
                                                            EqualTo(fieldname="email", message="Emails don't match.")])
    password = PasswordField("Password",
                             description='Password must include: 1 uppercase letter, 1 lowercase letter, 1 number, '
                                         'and 1 special character',
                             validators=[DataRequired(message="Please fill in this field"),
                                         Length(min=7, max=50),
                                         EqualTo(fieldname="confirm_password",
                                                 message="Passwords don't match.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="Please fill in this field"),
                                                                     EqualTo(fieldname="password",
                                                                             message="Passwords don't match.")])
    submit = SubmitField("Register")  # may not be needed

    def validate_password(form, field):
        """
        Validate password meets minimum requirements
        Valid passwords contain:
        - 8 to 30 characters
        - 1 digit or more
        - 1 symbol or more
        - 1 uppercase letter or more
        - 1 lowercase letter or more
        :param field: password field
        :returns: None. raises ValidationErrors with exception messages, or passes
        """
        reg_exp = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%!^&+=]).*$"
        reg = re.compile(reg_exp)
        if not re.search(reg, field.data):
            raise ValidationError("Password must include: "
                                  "1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character")

    def validate_email(form, field):
        """
        Custom email validator
            Check if the email is valid and if the email already has an account
            Try to get any existing account information for that email
            using Flask-Login's authentication. Handle all exceptions, but
            if the user is not found then they may successfully pass this validation
        :param field: the form field in question, in this case email
        :returns: None. raises ValidationErrors with exception messages, or passes
        """
        found = True
        try:
            emailObj = email_validator.validate_email(field.data)
            auth.get_user_by_email(emailObj.email)
        except email_validator.EmailNotValidError as err:
            raise ValidationError(str(err))
        except ValueError as verr:
            raise ValidationError(str(verr))
        except auth.UserNotFoundError:
            found = False  # If user isn't found, they don't already have an account.
        except:
            raise ValidationError("Error. Please try a different email.")
        if found:
            raise ValidationError("Email already in use.")


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
    weight = IntegerField("Weight (lbs.)", [DataRequired(),
                                            NumberRange(min=0, max=5000,
                                                        message='Must be a number between 0-5000.')])

    height_feet = SelectField("Ft.", [DataRequired()], choices=['3\'', '4\'', '5\'', '6\'', '7\''])

    height_inches = SelectField("Inches", [DataRequired()], choices=['1"', '2"', '3"', '4"', '5"', '6"', '7"',
                                                                     '8"', '9"', '10"', '11"'])

    activity = SelectField("Activity Level", [DataRequired()], choices=["Very Active", "Moderately Active",
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


class MyGoals(FlaskForm):
    """
    Form for creating and updating goals in My Goals
    """

    goal_id = StringField("Goal ID", validators=[DataRequired()])

    goal_name = StringField("Goal Name",
                            validators=[DataRequired(),
                                        Length(min=1, max=50, message='Name must be between 1-50 characters long')])
    calories = IntegerField("Calories",
                            validators=[DataRequired(), NumberRange(min=1000, max=10000,
                                                                    message='Must be a number between 1000-10000.')])
    carb_goal = IntegerField("Carb Goal",
                             validators=[DataRequired(), NumberRange(min=0, max=2500,
                                                                     message='Must be a number between 0-2500.')])
    fat_goal = IntegerField("Fat Goal",
                            validators=[DataRequired(), NumberRange(min=0, max=1500,
                                                                    message='Must be a number between 0-2500.')])
    protein_goal = IntegerField("Protein Goal",
                                validators=[DataRequired(), NumberRange(min=0, max=2500,
                                                                        message='Must be a number between 0-2500.')])
    number_of_meals = IntegerField("Number of Meals", validators=[DataRequired(), NumberRange(min=1, max=25,
                                                                                        message='Must be a number between 1-25.')])
    desired_weight = IntegerField("Desired Weight",
                                  validators=[DataRequired(), NumberRange(min=25, max=2000,
                                                                          message='Must be a number between 25-2000.')])
    submit = SubmitField("Save")

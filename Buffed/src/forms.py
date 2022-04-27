import re
import email_validator
from firebase_admin import auth
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField, PasswordField, DateField, DecimalField, \
    RadioField, SelectMultipleField, widgets, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Regexp, NumberRange, Length, EqualTo, ValidationError


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


class RegisterForm(FlaskForm):
    # TODO: implement more robust email and password requirements and validation
    email = EmailField("Email", validators=[DataRequired(message="Please fill in this field"),
                                            Email(check_deliverability=True), Length(min=7, max=50),
                                            EqualTo(fieldname="confirm_email", message="Emails don't match.")])
    confirm_email = EmailField("Confirm Email", validators=[DataRequired(message="Please fill in this field"), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(message="Please fill in this field"),
                                         Length(min=7, max=50),
                                         EqualTo(fieldname="confirm_password",
                                                 message="Passwords don't match.")])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(message="Please fill in this field")])
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
        """
        reg_exp = "^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%!^&+=]).*$"
        reg = re.compile(reg_exp)
        if not re.search(reg, field.data):
            raise ValidationError("Password must include:"
                                  "1 uppercase letter, 1 lowercase letter, 1 digit, and 1 special character")

    def validate_email(form, field):
        """
        Custom email validator
            Check if the email is valid and if the email already has an account
            Try to get any existing account information for that email
            using Flask-Login's authentication. Handle all exceptions, but
            if the user is not found then they may successfully pass this validation
        :param field: the form field in question, in this case email
        :returns: Nothing. raises ValidationErrors with exception messages, or passes
        """
        try:
            emailObj = email_validator.validate_email(field.data)
            auth.get_user_by_email(emailObj.email)
        except email_validator.EmailNotValidError as err:
            raise ValidationError(str(err))
        except ValueError as verr:
            raise ValidationError(str(verr))
        except auth.UserNotFoundError:
            pass  # If user isn't found, they don't already have an account.
        except auth.EmailAlreadyExistsError:
            raise ValidationError("Email already in use.")
        except:
            raise ValidationError("Error. Please try a different email.")



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


class EditProfile(FlaskForm):
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
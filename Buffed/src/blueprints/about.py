from flask import Blueprint, render_template, request, flash

from src.forms import ContactForm

about_page = Blueprint("about", __name__, static_folder="static", template_folder="templates")


def send_contact(result):
    """
        Takes a posted contact email result from about's contact form
        and sends the email.
        :return: None
    """
    # TODO: Implement Contact form functionality that sends email to server?
    # This is for a User Story that's in the icebox currently (noted 3/17/2022)
    pass


@about_page.route('/', methods=["GET", "POST"])
def about():
    """
        This method returns the about us page and handles any posted contact form info.
        :return: renders template for about.html with contact form
    """
    form = ContactForm()

    # validate_on_submit checks for submission with POST method,
    # then calls validate() to trigger form validation
    if form.validate_on_submit():
        # if a contact form is posted, store email information as result
        result = {'name': request.form["name"],
                  'email': request.form["email"],
                  'subject': request.form["subject"],
                  'message': request.form["message"]}

        # Send this email result using send_contact method
        send_contact(result)

        # resume as normal (re-render about.html page with form after sending)
        return render_template('about.html', form=form)
    else:
        # render template with contact form
        return render_template('about.html', form=form)

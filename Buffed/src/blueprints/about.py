from flask import Blueprint, render_template, request
from Buffed.src.forms import ContactForm

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
        :return: render_template('about.html')
    """
    form = ContactForm()

    if request.method == 'POST':
        # if an email is posted, store email information as result
        result = {'name': request.form["name"],
                  'email': request.form["email"],
                  'subject': request.form["subject"],
                  'message': request.form["message"]}

        # Send this email result using send_contact method
        send_contact(result)

        # resume as normal (show about.html page with form after sending)
        return render_template('about.html', form=form)
    else:
        return render_template('about.html', form=form)

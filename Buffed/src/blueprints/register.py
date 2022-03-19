from flask import Blueprint, render_template

register_page = Blueprint("register", __name__, static_folder="static", template_folder="templates")


@register_page.route('/')
def register():
    """
        This method returns the register page.
        :return: render_template('register.html')
        """
    return render_template('register.html')

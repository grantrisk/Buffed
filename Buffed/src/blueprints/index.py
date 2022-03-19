from flask import Blueprint, render_template

index_page = Blueprint("index", __name__, static_folder="static", template_folder="templates")


@index_page.route('/')
def index():
    """
    This method returns the index page.
    :return: render_template('index.html')
    """
    return render_template('index.html')

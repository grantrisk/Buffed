from flask import Blueprint, render_template
from flask_login import login_required

dashboard_page = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


@login_required
@dashboard_page.route('/')
def dashboard():
    """
        This method returns the page for the dashboard.
        :return: render_template('dashboard.html')
        """
    return render_template('dashboard.html')

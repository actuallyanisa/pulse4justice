from website.views import views


from flask import render_template
from flask_login import current_user


@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html", user=current_user)

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():

    return render_template("home.html")

@views.route('/donate')
def donate():
    return render_template('donate.html')

@views.route('/updates')
def updates():
    return render_template('updates.html')
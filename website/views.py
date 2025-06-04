import os
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, render_template
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db

views = Blueprint('views', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # Set default image
    image_filename = f"{current_user.id}.jpg"
    upload_folder = current_app.config['UPLOAD_FOLDER']
    user_image_path = os.path.join(upload_folder, image_filename)

    # If user hasn't uploaded a profile picture, use default
    user_image_path = os.path.join(upload_folder, image_filename)

    if not os.path.exists(user_image_path):
        image_filename = 'default.jpg'
        print("Looking for file at:", user_image_path)

    profile_image = url_for('static', filename=f'images/{image_filename}')

    if request.method == 'POST':
        file = request.files.get('profile-pic')
        if file and allowed_file(file.filename):
            os.makedirs(upload_folder, exist_ok=True)  # create folder if missing
            filename = secure_filename(f"{current_user.id}.jpg")
            file.save(os.path.join(upload_folder, filename))
            return redirect(url_for('views.profile'))

    return render_template('profile.html', profile_image=profile_image)

@views.route('/update-password', methods=['POST'])
@login_required
def update_password():
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    if not check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for('views.profile'))

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('views.profile'))

    current_user.password = generate_password_hash(new_password)
    db.session.commit()
    flash("Password updated successfully.", "success")
    return redirect(url_for('views.profile'))

@views.route('/')
def home():
    return render_template("home.html")


@views.route('/donate')
def donate():
    return render_template('donate.html')

@views.route('/aboutus')
def updates():
    return render_template('aboutus.html')

@views.route('/shareyourstory')
def shareyourstory():
    return render_template('shareyourstory.html')

@views.route('/error')
def error():
    return render_template('error.html')

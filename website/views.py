import os
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, render_template
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db
from stripe_config import stripe
from flask import send_from_directory
from dotenv import load_dotenv
from .models import Fundraiser

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")



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

@views.route('/update-email', methods=['POST'])
@login_required
def update_email():
    print("Update email form submitted")
    print("Form data:", request.form)

    current_email = request.form.get('current_email')
    new_email = request.form.get('new_email')

    print("Entered current_email:", current_email)
    print("Logged-in user's email:", current_user.email)

    if current_user.email != current_email:
        flash("Current email is incorrect.", "danger")
        return redirect(url_for('views.profile'))

    current_user.email = new_email
    db.session.commit()
    flash("Email updated successfully!", "success")
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
@login_required
def shareyourstory():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_story = Fundraiser(title=title, description=description, user_id=current_user.id)
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('views.view_story', fundraiser_id=new_story.id))
    return render_template('shareyourstory.html')

@views.route('/error')
def error():
    return render_template('error.html')

@views.route('/signup')
def signup():
    return render_template('sign_up.html')

@views.route('/account_link', methods=['POST'])
def create_account_link():
    try:
        connected_account_id = request.get_json().get('account')

        account_link = stripe.AccountLink.create(
          account=connected_account_id,
          return_url=f"http://localhost:4242/return/{connected_account_id}",
          refresh_url=f"http://localhost:4242/refresh/{connected_account_id}",
          type="account_onboarding",
        )

        return jsonify({
          'url': account_link.url,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account link: ', e)
        return jsonify(error=str(e)), 500
    
@views.route('/connect')
def connect():
    return render_template('index.html')

@views.route('/account', methods=['POST'])
def create_account():
    try:
        account = stripe.Account.create(
          controller={
            "stripe_dashboard": {
              "type": "express",
            },
            "fees": {
              "payer": "application"
            },
            "losses": {
              "payments": "application"
            },
          },
        )

        return jsonify({
          'account': account.id,
        })
    except Exception as e:
        print('An error occurred when calling the Stripe API to create an account: ', e)
        return jsonify(error=str(e)), 500

@views.route('/', defaults={'path': ''})

# Flask does not like serving static files with a sub-path, so just force them to serve up the frontend here
@views.route('/return/<path>')
@views.route('/refresh/<path>')
@views.route('/<path:path>')
def catch_all(path, **kwargs):
        if path and os.path.exists(os.path.join(views.static_folder, path)):
            return send_from_directory(views.static_folder, path)
        else:
            return send_from_directory(views.static_folder, 'index.html')

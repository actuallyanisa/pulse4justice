import os
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app, flash, render_template
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from .models import User
from . import db
from flask import send_from_directory
from dotenv import load_dotenv
from .models import Fundraiser
from flask_login import login_user


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

@views.route('/form')
@login_required
def form():
    return render_template('form.html')
    

@views.route('/error')
def error():
    return render_template('error.html')

@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(password1) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            # create new user
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()

            # log the user in right away
            login_user(new_user, remember=True)

            flash('Account created and logged in!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html')



@views.route('/lgbtqiadiscrimination')
def lgbtqiadiscrimination():
    return render_template('lgbtqiadiscrimination.html')

@views.route('/ableism')
def ableism():
    return render_template('ableism.html')

@views.route('/religiousdiscrimination')
def religiousdiscrimination():
    return render_template('religiousdiscrimination.html')

@views.route('/classism')
def classism():
    return render_template('classism.html')

@views.route('/sexism')
def sexism():
    return render_template('sexism.html')

@views.route('/racism')
def racism():
    return render_template('racism.html')

@views.route('/mentalhealthstigmatization')
def mentalhealthstigmatization():
    return render_template('mentalhealthstigmatization.html')

@views.route('/linguisticdiscrimination')
def linguisticdiscrimination():
    return render_template('linguisticdiscrimination.html')

@views.route('/ageism')
def ageism():
    return render_template('ageism.html')

from flask_mail import Message
from . import mail

@views.route('/submit', methods=['POST'])
@login_required  # optionally require login if you want
def submit():
    data = request.form.to_dict(flat=False)

    # Extract fields like you do in previous example
    title = data.get('title', [''])[0]
    category = data.get('category', [''])[0]
    goal = data.get('goal', [''])[0]
    location = data.get('location', [''])[0]
    beneficiary = data.get('beneficiary', [''])[0]

    gender = data.get('gender', [''])[0]
    race = data.get('race', [''])[0]
    sexualOrientation = data.get('sexualOrientation', [''])[0]
    disabilities = data.get('disabilities', [''])[0]
    otherInfo = data.get('otherInfo', [''])[0]

    paypal = data.get('paypal', [''])[0]

    organizerName = data.get('organizerName', [''])[0]
    organizerEmail = data.get('organizerEmail', [''])[0]
    organizerPhone = data.get('organizerPhone', [''])[0]
    relationship = data.get('relationship', [''])[0]

    story = data.get('story', [''])[0]

    items = data.get('item[]', [])
    descriptions = data.get('description[]', [])
    costs = data.get('cost[]', [])

    wishlist_text = ""
    for i in range(len(items)):
        item = items[i] if i < len(items) else ''
        desc = descriptions[i] if i < len(descriptions) else ''
        cost = costs[i] if i < len(costs) else ''
        wishlist_text += f" - {item}: {desc}, Estimated cost: {cost}\n"
    if not wishlist_text:
        wishlist_text = "No wishlist items provided."

    email_body = f"""
New Fundraiser Submission:

Title: {title}
Category: {category}
Fundraising Goal: {goal}
Location: {location}
Beneficiary: {beneficiary}

Personal Details:
- Gender: {gender}
- Race/Ethnicity: {race}
- Sexual Orientation: {sexualOrientation}
- Disabilities or Accessibility Needs: {disabilities}
- Other Info: {otherInfo}

PayPal Email: {paypal}

Organizer Information:
- Name: {organizerName}
- Email: {organizerEmail}
- Phone: {organizerPhone}
- Relationship to Beneficiary: {relationship}

Wishlist:
{wishlist_text}

Story:
{story}
    """

    try:
        msg = Message(
            subject="New Fundraiser Submission",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[current_app.config['MAIL_USERNAME']],
            body=email_body
        )
        mail.send(msg)
        flash("Form submitted successfully!", "success")
        return redirect(url_for('views.home'))
    except Exception as e:
        flash(f"Failed to send email: {str(e)}", "danger")
        return redirect(url_for('views.form'))
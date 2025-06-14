import os
from os import path
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import stripe
from werkzeug.exceptions import RequestEntityTooLarge

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change to your own secret!
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)
    migrate.init_app(app, db)  # <-- This enables flask db commands

    # Import blueprints and models AFTER db initialization
    from .views import views as views_blueprint
    from .auth import auth
    from .models import User

    app.register_blueprint(views_blueprint)
    app.register_blueprint(auth)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return render_template("error.html", error_message="Your profile picture must be smaller than 2MB."), 413

    @app.context_processor
    def inject_user():
        if current_user.is_authenticated:
            image_filename = f"{current_user.id}.jpg"
            image_path = os.path.join(app.static_folder, 'images', image_filename)
            if not os.path.exists(image_path):
                image_filename = 'default.jpg'
            profile_image = url_for('static', filename=f'images/{image_filename}')
        else:
            profile_image = url_for('static', filename='images/default.jpg')
        return dict(user=current_user, profile_image=profile_image)

    # Set Stripe API key from environment
    stripe_key = os.getenv('STRIPE_SECRET_KEY')
    if not stripe_key:
        raise Exception("Stripe API key not set in environment variable STRIPE_SECRET_KEY")
    stripe.api_key = stripe_key

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

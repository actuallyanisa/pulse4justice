import os
from flask import Flask, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from dotenv import load_dotenv
from os import path

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'

    # DB config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Mail config
    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'rohini@pulseforjustice.org'
    app.config['MAIL_PASSWORD'] = 'PulseForJusticeColdEmail10!'  # Use env var in prod

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from .views import views
    from .auth import auth  # Your auth blueprint, if exists

    app.register_blueprint(views)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User  # your User model

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_user():
        if current_user.is_authenticated:
            profile_image = url_for('static', filename=f'images/{current_user.id}.jpg')
        else:
            profile_image = url_for('static', filename='images/default.jpg')
        return dict(user=current_user, profile_image=profile_image)

    with app.app_context():
        db.create_all()

    return app

def create_database(app):
    DB_NAME = 'database.db'  # Define the database name
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        

from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')
    app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    # Import blueprints and models AFTER db init
    from .views import views as views_blueprint
    from .auth import auth
    from .models import User

    from .auth import auth

    app.register_blueprint(views_blueprint, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    from .models import User

    with app.app_context():
        db.create_all()

    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    from werkzeug.exceptions import RequestEntityTooLarge
    from flask import jsonify, render_template

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        return render_template("error.html", error_message="Your profile picture must be smaller than 2MB."), 413

    @app.context_processor
    def inject_user():
        from flask_login import current_user
        import os
        from flask import url_for

        if current_user.is_authenticated:
            image_filename = f"{current_user.id}.jpg"
            image_path = os.path.join(app.static_folder, 'images', image_filename)
            if not os.path.exists(image_path):
                image_filename = 'default.jpg'
            profile_image = url_for('static', filename=f'images/{image_filename}')
        else:
            profile_image = url_for('static', filename='images/default.jpg')

        return dict(user=current_user, profile_image=profile_image)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

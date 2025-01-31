from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

# Initialize the SQLAlchemy object
db = SQLAlchemy()

# Set the name of the SQLite database
DB_NAME = 'webapp1.sqlite'

# Function to create the database
def create_database(app):
    if not os.path.exists(DB_NAME):  # Check if the database file exists
        with app.app_context():  # Ensure this runs in the app context
            try:
                db.create_all()
                print("Database created!")
            except Exception as e:
                print(f"Error creating the database: {e}")
    else:
        print("Database already exists!")

# Function to initialize the Flask app
def create_app():
    # Create a Flask app instance
    app = Flask(__name__)

    # Load configuration values (from environment variables or defaults)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', f'sqlite:///{DB_NAME}')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking (optional)

    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')
    
    
    login_manager=LoginManager()
    login_manager.init_app(app)
    login_manager.login_view='auth.login'
    # Import blueprints (make sure to replace with actual imports)
    from .views import views
    from .auth import auth
    from .admin import admin
    from .models import Customer,Cart,Product,Order
    # Register the blueprints with the app
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    # with app.app_context():
    #     create_database(app)
   

    @login_manager.user_loader
    def load_user(user_id):
        return Customer.query.get(int(user_id))  # Retrieve 
    # Return the app instance
    return app

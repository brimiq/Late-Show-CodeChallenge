"""
Late Show API - Main Application

This is the main entry point for the Flask application.
It initializes the database and registers all blueprints/routes.

To run the application:
    python app.py

The API will be available at http://localhost:5000
"""

from flask import Flask
from flask_migrate import Migrate

# Import configuration
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

# Import models and database
from models import db

# Import API routes blueprint
from routes import api


def create_app():
    """
    Application Factory Pattern
    
    Creates and configures the Flask application.
    This pattern allows for multiple instances of the app
    with different configurations if needed.
    
    Returns:
        Flask: The configured Flask application
    """
    app = Flask(__name__)
    
    # Configure the application
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Initialize database with app
    db.init_app(app)
    
    # Initialize Flask-Migrate for database migrations
    migrate = Migrate(app, db)
    
    # Register the API blueprint with URL prefix
    # All routes in routes.py will be prefixed with /api
    app.register_blueprint(api, url_prefix='/')
    
    # Add a root route to verify the app is running
    @app.route('/')
    def index():
        """Root endpoint to verify API is running"""
        return {
            'message': 'Welcome to the Late Show API',
            'status': 'running',
            'endpoints': {
                'episodes': '/episodes',
                'episode_detail': '/episodes/<id>',
                'guests': '/guests',
                'appearances': '/appearances'
            }
        }
    
    return app


# Create the application instance
app = create_app()


if __name__ == '__main__':
    """
    Main entry point when running the script directly
    
    Development server configuration:
    - host='0.0.0.0': Make the server publicly available
    - port=5000: Default Flask development port
    - debug=True: Enable debug mode for development
    """
    app.run(host='0.0.0.0', port=5000, debug=True)


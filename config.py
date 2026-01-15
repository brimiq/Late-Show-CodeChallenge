"""
Flask Application Configuration
"""
import os

# Base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Database Configuration
# Using SQLite for simplicity in development
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'late_show.db')

# Disable Flask-SQLAlchemy track modifications
# (saves memory when not needed)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Secret key for session management
# In production, use environment variable
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-prod'

# API Pagination settings
API_DEFAULT_PAGE_SIZE = 10
API_MAX_PAGE_SIZE = 100


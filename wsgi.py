#!/usr/bin/env python3
"""
WSGI entry point for the Resume Modifier application.
This file is used to run the Flask application in production.
"""

import os
import sys

# Add the project root to Python path
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir)
# Add the core directory to allow 'app' imports (fixes ModuleNotFoundError: No module named 'app')
sys.path.insert(0, os.path.join(basedir, 'core'))

# Import the app factory and db
# Use 'app' directly since we added core to path, this aligns with how internal imports work
from app import create_app, db

# Create the Flask application instance
app = create_app()


if __name__ == "__main__":
    # Development server
    # Initialize database tables
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)
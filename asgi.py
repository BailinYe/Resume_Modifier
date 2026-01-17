#!/usr/bin/env python3
"""
ASGI entry point for the Resume Modifier FastAPI application.
This file is used to run the FastAPI application in production with uvicorn.
"""

import os
import sys

# Add the project root to Python path
basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir)
# Add the core directory to allow 'app' imports
sys.path.insert(0, os.path.join(basedir, 'core'))

# Import the FastAPI app
from app.main import app

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    workers = int(os.environ.get('WORKERS', 1))
    
    uvicorn.run(
        "asgi:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info"
    )

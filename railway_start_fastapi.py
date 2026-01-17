#!/usr/bin/env python3
"""
Railway deployment entry point for Resume Modifier (FastAPI版本)
Handles proper Python path setup for module imports
"""

import sys
import os

# Add the core directory to Python path (where the app module is located)
current_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(current_dir, 'core')
sys.path.insert(0, core_dir)

# Also add current directory for any root-level imports
sys.path.insert(0, current_dir)

# Set environment variables
os.environ.setdefault('PYTHONPATH', f"{core_dir}:{current_dir}")

# Change working directory to core for Alembic to find migrations
os.chdir(core_dir)

if __name__ == "__main__":
    try:
        # Import uvicorn and the FastAPI application
        import uvicorn
        from app.main import app
        
        # Get port from environment (Railway sets this automatically)
        port = int(os.environ.get('PORT', 5001))
        host = os.environ.get('HOST', '0.0.0.0')
        workers = int(os.environ.get('WORKERS', 1))
        
        print(f"🚀 Starting Resume Modifier (FastAPI) on {host}:{port}")
        print(f"📍 Python Path: {sys.path[0]}")
        print(f"🔧 Working Directory: {os.getcwd()}")
        print(f"📦 FastAPI App: {app}")
        print(f"👷 Workers: {workers}")
        
        # Start the application with uvicorn
        uvicorn.run(
            app,
            host=host,
            port=port,
            workers=workers,
            log_level="info",
            access_log=True
        )
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print(f"📂 Current directory: {os.getcwd()}")
        print(f"📁 Directory contents: {os.listdir('.')}")
        if os.path.exists('app'):
            print(f"📁 App directory contents: {os.listdir('app')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Startup Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

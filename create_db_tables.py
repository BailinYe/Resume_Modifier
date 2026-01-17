#!/usr/bin/env python
"""
快速创建数据库表
"""
import sys
import os

# 添加 core 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from app import create_app
from app.extensions import db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        print("\nYou can now start the server with:")
        print("  python railway_start.py")

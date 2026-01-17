#!/usr/bin/env python
"""
创建测试用户
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from app import create_app
from app.extensions import db
from app.models.temp import User

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # 检查用户是否已存在
        existing_user = User.query.filter_by(email='test@example.com').first()
        if existing_user:
            print("⚠️  Test user already exists!")
            print(f"Email: {existing_user.email}")
        else:
            # 创建测试用户
            test_user = User(
                username='testuser',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
            test_user.set_password('password123')  # 正确的密码设置方法
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully!")
            print("Email: test@example.com")
            print("Password: password123")

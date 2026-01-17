#!/usr/bin/env python
"""
测试一份简历多岗位修改功能
"""
import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from app import create_app
from app.extensions import db
from app.models.temp import User, Resume, JobDescription, ResumeTemplate
from datetime import datetime

def create_test_data():
    """创建测试数据"""
    app = create_app()
    with app.app_context():
        # 获取测试用户
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            print("❌ 测试用户不存在，请先运行 create_test_user.py")
            return None
        
        print(f"✅ 找到用户: {user.email} (ID: {user.id})")
        
        # 创建默认模板（如果不存在）
        template = ResumeTemplate.query.filter_by(id=1).first()
        if not template:
            template = ResumeTemplate(
                id=1,
                name="默认模板",
                description="简洁专业的默认简历模板",
                style_config={"font": "Arial", "fontSize": 12},
                sections=["personalInfo", "summary", "experience", "skills"],
                is_active=True
            )
            db.session.add(template)
            db.session.commit()
            print("✅ 创建默认模板")
        else:
            print(f"✅ 找到现有模板: {template.name}")
        
        # 创建测试简历
        existing_resume = Resume.query.filter_by(user_id=user.id, serial_number=1).first()
        if not existing_resume:
            test_resume = Resume(
                user_id=user.id,
                serial_number=1,
                title="张三的软件工程师简历",
                parsed_resume={
                    "personalInfo": {
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "phone": "13800138000"
                    },
                    "professionalSummary": "5年Python开发经验，熟悉Web开发和数据分析",
                    "workExperience": [
                        {
                            "company": "XX科技公司",
                            "position": "Python开发工程师",
                            "duration": "2020-2024",
                            "description": "负责后端API开发和数据库优化"
                        }
                    ],
                    "skills": ["Python", "Flask", "Django", "PostgreSQL", "Docker"],
                    "projects": [
                        {
                            "name": "电商平台",
                            "description": "使用Django开发的在线商城系统"
                        }
                    ]
                },
                template_id=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(test_resume)
            print("✅ 创建测试简历")
        else:
            print(f"✅ 找到现有简历: {existing_resume.title}")
        
        # 创建测试职位描述
        job_titles = [
            ("后端开发工程师", "负责公司核心业务系统的后端开发，要求熟悉Python、Flask框架、PostgreSQL数据库、RESTful API设计"),
            ("全栈工程师", "负责Web应用的前后端开发，要求掌握Python、JavaScript、React、Django、MySQL"),
            ("数据工程师", "负责数据管道搭建和ETL开发，要求熟悉Python、SQL、Spark、Airflow、数据仓库")
        ]
        
        for idx, (title, desc) in enumerate(job_titles, 1):
            existing_job = JobDescription.query.filter_by(
                user_id=user.id,
                serial_number=idx
            ).first()
            
            if not existing_job:
                job = JobDescription(
                    user_id=user.id,
                    serial_number=idx,
                    title=title,
                    description=desc,
                    created_at=datetime.utcnow()
                )
                db.session.add(job)
                print(f"✅ 创建职位描述 {idx}: {title}")
            else:
                print(f"✅ 找到现有职位: {existing_job.title}")
        
        db.session.commit()
        print("\n📊 测试数据准备完成！")
        return user.id

if __name__ == '__main__':
    create_test_data()

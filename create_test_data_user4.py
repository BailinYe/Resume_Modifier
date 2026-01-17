#!/usr/bin/env python3
"""为用户4创建测试数据"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from app import create_app
from app.extensions import db
from app.models.temp import User, Resume, JobDescription, ResumeTemplate
from datetime import datetime

def create_test_data_for_user4():
    app = create_app()
    with app.app_context():
        # 查找用户4
        user = User.query.filter_by(id=4).first()
        if not user:
            print("❌ 用户4不存在")
            return
        
        print(f"✅ 找到用户: {user.email} (ID: {user.id})")
        
        # 确保模板存在
        template = ResumeTemplate.query.filter_by(id=1).first()
        if not template:
            print("❌ 模板不存在，请先运行 create_test_data.py")
            return
        
        # 创建简历
        resume = Resume(
            user_id=user.id,
            serial_number=1,
            title="用户4的软件工程师简历",
            parsed_resume={
                "personalInfo": {
                    "name": "李四",
                    "email": user.email,
                    "phone": "13900139000"
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
        db.session.add(resume)
        
        # 创建职位描述
        jobs = [
            ("后端开发工程师", "负责公司核心业务系统的后端开发，要求熟悉Python、Flask框架、PostgreSQL数据库、RESTful API设计"),
            ("全栈工程师", "负责Web应用的前后端开发，要求掌握Python、JavaScript、React、Django、MySQL"),
            ("数据工程师", "负责数据管道搭建和ETL开发，要求熟悉Python、SQL、Spark、Airflow、数据仓库")
        ]
        
        for idx, (title, desc) in enumerate(jobs, 1):
            job = JobDescription(
                user_id=user.id,
                serial_number=idx,
                title=title,
                description=desc,
                created_at=datetime.utcnow()
            )
            db.session.add(job)
        
        db.session.commit()
        print("✅ 测试数据创建成功！")
        print(f"   - 简历ID: 1")
        print(f"   - 职位ID: 1, 2, 3")

if __name__ == '__main__':
    create_test_data_for_user4()

"""
Batch Resume Modification Service
批量简历修改服务 - 根据不同职位描述批量修改多份简历
"""

import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from flask import current_app
from app.models.temp import Resume, JobDescription, User
from app.services.resume_ai import ResumeAI
from app.extensions import db
import logging

logger = logging.getLogger(__name__)


class BatchResumeModifier:
    """批量简历修改服务类"""
    
    def __init__(self):
        """初始化批量简历修改服务"""
        self.logger = logger
        
    def batch_modify_resumes(
        self, 
        resume_ids: List[int], 
        job_description_id: int,
        user_id: int,
        customization_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        批量修改简历 - 根据职位描述修改多份简历
        
        Args:
            resume_ids: 要修改的简历ID列表
            job_description_id: 职位描述ID
            user_id: 用户ID
            customization_options: 可选的自定义选项
            
        Returns:
            包含所有修改后简历的字典
        """
        try:
            # 验证用户权限
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            # 获取职位描述
            job_desc = JobDescription.query.filter_by(
                user_id=user_id, 
                serial_number=job_description_id
            ).first()
            
            if not job_desc:
                raise ValueError(f"Job description {job_description_id} not found for user {user_id}")
            
            job_description_text = job_desc.description
            
            # 存储所有修改结果
            results = {
                'job_description_id': job_description_id,
                'job_description_title': job_desc.title,
                'total_resumes': len(resume_ids),
                'successful_modifications': 0,
                'failed_modifications': 0,
                'modified_resumes': [],
                'errors': [],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # 遍历每个简历并进行修改
            for idx, resume_id in enumerate(resume_ids):
                try:
                    self.logger.info(f"Processing resume {idx + 1}/{len(resume_ids)}: ID {resume_id}")
                    
                    # 修改单个简历
                    modified_result = self._modify_single_resume(
                        user_id=user_id,
                        resume_id=resume_id,
                        job_description=job_description_text,
                        job_title=job_desc.title,
                        customization_options=customization_options
                    )
                    
                    results['modified_resumes'].append(modified_result)
                    results['successful_modifications'] += 1
                    
                except Exception as e:
                    error_msg = f"Failed to modify resume {resume_id}: {str(e)}"
                    self.logger.error(error_msg)
                    results['errors'].append({
                        'resume_id': resume_id,
                        'error': error_msg
                    })
                    results['failed_modifications'] += 1
            
            return results
            
        except Exception as e:
            self.logger.error(f"Batch modification error: {str(e)}")
            raise
    
    def _modify_single_resume(
        self,
        user_id: int,
        resume_id: int,
        job_description: str,
        job_title: str,
        customization_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        修改单个简历以匹配职位描述
        
        Args:
            user_id: 用户ID
            resume_id: 简历ID
            job_description: 职位描述文本
            job_title: 职位标题
            customization_options: 自定义选项
            
        Returns:
            修改后的简历数据
        """
        # 查询简历
        resume = Resume.query.filter_by(
            user_id=user_id,
            serial_number=resume_id
        ).first()
        
        if not resume:
            raise ValueError(f"Resume {resume_id} not found for user {user_id}")
        
        # 获取原始简历数据
        original_resume = resume.parsed_resume
        
        # 创建AI处理器
        resume_ai = ResumeAI("")
        resume_ai.parsed_resume = original_resume
        
        # 分析简历与职位的匹配度
        analysis = resume_ai.analyze(job_description)
        
        # 根据职位描述优化简历
        optimized_resume = self._optimize_resume_for_job(
            original_resume=original_resume,
            job_description=job_description,
            analysis=analysis,
            customization_options=customization_options
        )
        
        # 生成修改后的简历标题
        modified_title = self._generate_modified_title(
            original_title=resume.title,
            job_title=job_title
        )
        
        return {
            'original_resume_id': resume_id,
            'original_title': resume.title,
            'modified_title': modified_title,
            'original_content': original_resume,
            'modified_content': optimized_resume,
            'analysis': analysis,
            'match_score': analysis.get('overallScore', 0),
            'modifications_summary': self._generate_modifications_summary(
                original_resume, 
                optimized_resume,
                analysis
            ),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _optimize_resume_for_job(
        self,
        original_resume: Dict[str, Any],
        job_description: str,
        analysis: Dict[str, Any],
        customization_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        根据职位描述优化简历内容
        
        Args:
            original_resume: 原始简历数据
            job_description: 职位描述
            analysis: 简历分析结果
            customization_options: 自定义选项
            
        Returns:
            优化后的简历数据
        """
        from openai import OpenAI
        
        # 复制原始简历作为基础
        optimized = json.loads(json.dumps(original_resume))
        
        # 配置优化级别
        options = customization_options or {}
        optimize_summary = options.get('optimize_summary', True)
        optimize_experience = options.get('optimize_experience', True)
        optimize_skills = options.get('optimize_skills', True)
        optimize_projects = options.get('optimize_projects', True)
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 优化个人简介/目标
        if optimize_summary and 'professionalSummary' in optimized:
            try:
                summary_prompt = f"""
                根据以下职位描述，优化简历的个人简介部分，使其更符合职位要求。
                
                原始个人简介:
                {optimized.get('professionalSummary', '')}
                
                职位描述:
                {job_description}
                
                要求:
                1. 突出与职位相关的技能和经验
                2. 使用职位描述中的关键词
                3. 保持专业且简洁（3-5句话）
                4. 只返回优化后的个人简介文本
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一位专业的简历优化专家。"},
                        {"role": "user", "content": summary_prompt}
                    ],
                    temperature=0.7
                )
                
                optimized['professionalSummary'] = response.choices[0].message.content.strip()
            except Exception as e:
                self.logger.warning(f"Failed to optimize summary: {str(e)}")
        
        # 优化工作经验描述
        if optimize_experience and 'workExperience' in optimized:
            try:
                for exp in optimized['workExperience']:
                    if 'description' in exp and exp['description']:
                        exp_prompt = f"""
                        优化以下工作经验描述，使其更符合目标职位要求。
                        
                        原始描述:
                        {exp['description']}
                        
                        职位名称: {exp.get('position', 'N/A')}
                        目标职位描述:
                        {job_description}
                        
                        要求:
                        1. 使用行动导向的动词开头
                        2. 包含可量化的成果
                        3. 突出与目标职位相关的技能
                        4. 使用职位描述中的关键词
                        5. 保持专业格式（每行一个bullet point）
                        6. 只返回优化后的描述文本（bullet points）
                        """
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "你是一位专业的简历优化专家。"},
                                {"role": "user", "content": exp_prompt}
                            ],
                            temperature=0.7
                        )
                        
                        exp['description'] = response.choices[0].message.content.strip()
            except Exception as e:
                self.logger.warning(f"Failed to optimize work experience: {str(e)}")
        
        # 优化技能部分
        if optimize_skills and 'skills' in optimized:
            try:
                # 从职位描述提取关键技能
                skills_prompt = f"""
                分析以下职位描述，提取关键技能要求，并将其与候选人的现有技能结合。
                
                候选人现有技能:
                {json.dumps(optimized['skills'], ensure_ascii=False)}
                
                职位描述:
                {job_description}
                
                要求:
                1. 保留候选人所有相关技能
                2. 添加职位描述中提到的候选人可能具备的技能
                3. 按重要性排序（最相关的放在前面）
                4. 只返回JSON数组格式的技能列表
                
                返回格式示例:
                ["Skill 1", "Skill 2", "Skill 3"]
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "你是一位专业的简历优化专家。返回纯JSON格式。"},
                        {"role": "user", "content": skills_prompt}
                    ],
                    temperature=0.7
                )
                
                content = response.choices[0].message.content.strip()
                # 清理可能的markdown格式
                content = content.replace("```json", "").replace("```", "").strip()
                optimized_skills = json.loads(content)
                
                if isinstance(optimized_skills, list):
                    optimized['skills'] = optimized_skills
            except Exception as e:
                self.logger.warning(f"Failed to optimize skills: {str(e)}")
        
        # 优化项目经验
        if optimize_projects and 'projects' in optimized:
            try:
                for project in optimized['projects']:
                    if 'description' in project and project['description']:
                        project_prompt = f"""
                        优化以下项目描述，使其更符合目标职位要求。
                        
                        原始描述:
                        {project['description']}
                        
                        项目名称: {project.get('name', 'N/A')}
                        目标职位描述:
                        {job_description}
                        
                        要求:
                        1. 突出项目中使用的相关技术
                        2. 强调项目成果和影响
                        3. 使用职位描述中的关键技术词汇
                        4. 保持简洁专业
                        5. 只返回优化后的描述文本
                        """
                        
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[
                                {"role": "system", "content": "你是一位专业的简历优化专家。"},
                                {"role": "user", "content": project_prompt}
                            ],
                            temperature=0.7
                        )
                        
                        project['description'] = response.choices[0].message.content.strip()
            except Exception as e:
                self.logger.warning(f"Failed to optimize projects: {str(e)}")
        
        return optimized
    
    def _generate_modified_title(self, original_title: str, job_title: str) -> str:
        """
        生成修改后的简历标题
        
        Args:
            original_title: 原始简历标题
            job_title: 职位标题
            
        Returns:
            修改后的标题
        """
        if job_title:
            return f"{original_title} - {job_title} Version"
        return f"{original_title} - Modified"
    
    def _generate_modifications_summary(
        self,
        original_resume: Dict[str, Any],
        modified_resume: Dict[str, Any],
        analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成修改摘要
        
        Args:
            original_resume: 原始简历
            modified_resume: 修改后简历
            analysis: 分析结果
            
        Returns:
            修改摘要
        """
        summary = {
            'sections_modified': [],
            'key_improvements': [],
            'match_score': analysis.get('overallScore', 0)
        }
        
        # 检查各部分是否被修改
        if original_resume.get('professionalSummary') != modified_resume.get('professionalSummary'):
            summary['sections_modified'].append('Professional Summary')
            summary['key_improvements'].append('优化个人简介以匹配职位要求')
        
        if original_resume.get('skills') != modified_resume.get('skills'):
            summary['sections_modified'].append('Skills')
            summary['key_improvements'].append('调整技能列表突出相关技能')
        
        if original_resume.get('workExperience') != modified_resume.get('workExperience'):
            summary['sections_modified'].append('Work Experience')
            summary['key_improvements'].append('优化工作经验描述增强相关性')
        
        if original_resume.get('projects') != modified_resume.get('projects'):
            summary['sections_modified'].append('Projects')
            summary['key_improvements'].append('调整项目描述突出相关技术')
        
        # 添加分析建议
        if 'recommendations' in analysis:
            summary['key_improvements'].extend(analysis['recommendations'][:3])
        
        return summary
    
    def modify_resume_for_multiple_jobs(
        self, 
        resume_id: int,
        job_description_ids: List[int],
        user_id: int,
        customization_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        根据多个职位描述修改一份简历 - 生成多个版本
        
        Args:
            resume_id: 要修改的简历ID
            job_description_ids: 职位描述ID列表
            user_id: 用户ID
            customization_options: 可选的自定义选项
            
        Returns:
            包含所有修改后简历版本的字典
        """
        try:
            # 验证用户权限
            user = User.query.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            # 验证简历存在
            resume = Resume.query.filter_by(
                user_id=user_id,
                serial_number=resume_id
            ).first()
            
            if not resume:
                raise ValueError(f"Resume {resume_id} not found for user {user_id}")
            
            # 存储所有修改结果
            results = {
                'original_resume_id': resume_id,
                'original_resume_title': resume.title,
                'total_job_positions': len(job_description_ids),
                'successful_modifications': 0,
                'failed_modifications': 0,
                'modified_versions': [],
                'errors': [],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # 遍历每个职位描述并生成对应的简历版本
            for idx, job_desc_id in enumerate(job_description_ids):
                try:
                    self.logger.info(f"Processing job position {idx + 1}/{len(job_description_ids)}: ID {job_desc_id}")
                    
                    # 获取职位描述
                    job_desc = JobDescription.query.filter_by(
                        user_id=user_id,
                        serial_number=job_desc_id
                    ).first()
                    
                    if not job_desc:
                        raise ValueError(f"Job description {job_desc_id} not found")
                    
                    # 修改简历以匹配此职位
                    modified_result = self._modify_single_resume(
                        user_id=user_id,
                        resume_id=resume_id,
                        job_description=job_desc.description,
                        job_title=job_desc.title,
                        customization_options=customization_options
                    )
                    
                    # 添加职位信息
                    modified_result['job_description_id'] = job_desc_id
                    modified_result['job_title'] = job_desc.title
                    
                    results['modified_versions'].append(modified_result)
                    results['successful_modifications'] += 1
                    
                except Exception as e:
                    error_msg = f"Failed to modify resume for job {job_desc_id}: {str(e)}"
                    self.logger.error(error_msg)
                    results['errors'].append({
                        'job_description_id': job_desc_id,
                        'error': error_msg
                    })
                    results['failed_modifications'] += 1
            
            return results
            
        except Exception as e:
            self.logger.error(f"Multi-job modification error: {str(e)}")
            raise

    def save_modified_resume(
        self,
        user_id: int,
        modified_resume_data: Dict[str, Any],
        save_as_new: bool = True
    ) -> Dict[str, Any]:
        """
        保存修改后的简历
        
        Args:
            user_id: 用户ID
            modified_resume_data: 修改后的简历数据
            save_as_new: 是否保存为新简历（默认为True）
            
        Returns:
            保存结果
        """
        try:
            if save_as_new:
                # 获取用户现有简历数量
                existing_count = Resume.query.filter_by(user_id=user_id).count()
                
                # 创建新简历
                new_resume = Resume(
                    user_id=user_id,
                    serial_number=existing_count + 1,
                    title=modified_resume_data['modified_title'],
                    parsed_resume=modified_resume_data['modified_content'],
                    template_id=1,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                db.session.add(new_resume)
                db.session.commit()
                
                return {
                    'success': True,
                    'resume_id': new_resume.serial_number,
                    'message': 'Modified resume saved as new resume'
                }
            else:
                # 更新现有简历
                resume = Resume.query.filter_by(
                    user_id=user_id,
                    serial_number=modified_resume_data['original_resume_id']
                ).first()
                
                if resume:
                    resume.title = modified_resume_data['modified_title']
                    resume.parsed_resume = modified_resume_data['modified_content']
                    resume.updated_at = datetime.utcnow()
                    db.session.commit()
                    
                    return {
                        'success': True,
                        'resume_id': resume.serial_number,
                        'message': 'Resume updated successfully'
                    }
                else:
                    raise ValueError("Resume not found")
                    
        except Exception as e:
            db.session.rollback()
            self.logger.error(f"Failed to save modified resume: {str(e)}")
            raise

"""
Batch Resume Modification Test Script
批量简历修改功能测试脚本
"""

import requests
import json
import time
from datetime import datetime


class BatchModificationTester:
    """批量简历修改功能测试类"""
    
    def __init__(self, base_url, username, password):
        """
        初始化测试器
        
        Args:
            base_url: API基础URL (例如: http://localhost:5000)
            username: 测试用户名
            password: 测试密码
        """
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.token = None
        self.headers = {}
    
    def login(self):
        """登录获取token"""
        print("🔐 登录中...")
        try:
            response = requests.post(
                f'{self.base_url}/api/login',
                json={
                    'username': self.username,
                    'password': self.password
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.headers = {
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                }
                print("✓ 登录成功!")
                return True
            else:
                print(f"✗ 登录失败: {response.status_code}")
                print(response.text)
                return False
        except Exception as e:
            print(f"✗ 登录错误: {str(e)}")
            return False
    
    def test_batch_modify(self, resume_ids, job_description_id):
        """
        测试批量修改简历
        
        Args:
            resume_ids: 简历ID列表
            job_description_id: 职位描述ID
        """
        print("\n📝 开始批量修改简历...")
        print(f"   简历IDs: {resume_ids}")
        print(f"   职位描述ID: {job_description_id}")
        
        try:
            payload = {
                'resume_ids': resume_ids,
                'job_description_id': job_description_id,
                'customization_options': {
                    'optimize_summary': True,
                    'optimize_experience': True,
                    'optimize_skills': True,
                    'optimize_projects': True
                },
                'save_as_new': True
            }
            
            start_time = time.time()
            
            response = requests.post(
                f'{self.base_url}/api/resume/batch-modify',
                headers=self.headers,
                json=payload
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"✓ 批量修改成功! (耗时: {elapsed_time:.2f}秒)")
                print(f"\n结果摘要:")
                print(f"  - 批次ID: {data.get('batch_id')}")
                print(f"  - 总简历数: {data['results']['total_resumes']}")
                print(f"  - 成功修改: {data['results']['successful_modifications']}")
                print(f"  - 失败修改: {data['results']['failed_modifications']}")
                
                # 显示每份简历的修改结果
                print(f"\n详细结果:")
                for i, resume in enumerate(data['results']['modified_resumes'], 1):
                    print(f"\n  简历 #{i}:")
                    print(f"    原标题: {resume['original_title']}")
                    print(f"    新标题: {resume['modified_title']}")
                    print(f"    匹配分数: {resume['match_score']}")
                    print(f"    修改部分: {', '.join(resume['modifications_summary']['sections_modified'])}")
                
                # 显示保存的新简历
                if data.get('saved_resumes'):
                    print(f"\n保存的新简历:")
                    for saved in data['saved_resumes']:
                        print(f"    ID {saved['original_id']} → ID {saved['new_id']}: {saved['title']}")
                
                return data.get('batch_id')
            else:
                print(f"✗ 批量修改失败: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"✗ 批量修改错误: {str(e)}")
            return None
    
    def test_get_batch_results(self, batch_id):
        """
        测试获取批量修改结果
        
        Args:
            batch_id: 批次ID
        """
        print(f"\n📊 获取批次 {batch_id} 的结果...")
        
        try:
            response = requests.get(
                f'{self.base_url}/api/resume/batch-modify/{batch_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✓ 成功获取批次结果!")
                print(f"\n批次信息:")
                print(f"  - 批次ID: {data['batch_id']}")
                print(f"  - 用户ID: {data['user_id']}")
                print(f"  - 职位标题: {data['job_title']}")
                print(f"  - 状态: {data['status']}")
                print(f"  - 创建时间: {data['created_at']}")
                print(f"  - 完成时间: {data['completed_at']}")
                print(f"  - 总简历数: {data['total_resumes']}")
                print(f"  - 成功: {data['successful_modifications']}")
                print(f"  - 失败: {data['failed_modifications']}")
                
                return True
            else:
                print(f"✗ 获取结果失败: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"✗ 获取结果错误: {str(e)}")
            return False
    
    def test_get_history(self, limit=10):
        """
        测试获取批量修改历史
        
        Args:
            limit: 返回记录数量
        """
        print(f"\n📜 获取批量修改历史 (最多{limit}条)...")
        
        try:
            response = requests.get(
                f'{self.base_url}/api/resume/batch-modify/history?limit={limit}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✓ 成功获取历史记录!")
                print(f"\n总记录数: {data['total_count']}")
                
                if data['batch_modifications']:
                    print(f"\n最近的批量修改:")
                    for i, batch in enumerate(data['batch_modifications'], 1):
                        print(f"\n  #{i} 批次 {batch['batch_id']}:")
                        print(f"      职位: {batch['job_title']}")
                        print(f"      简历数: {batch['total_resumes']}")
                        print(f"      成功: {batch['successful_modifications']}")
                        print(f"      状态: {batch['status']}")
                        print(f"      时间: {batch['created_at']}")
                else:
                    print("  (暂无历史记录)")
                
                return True
            else:
                print(f"✗ 获取历史失败: {response.status_code}")
                print(response.text)
                return False
                
        except Exception as e:
            print(f"✗ 获取历史错误: {str(e)}")
            return False
    
    def run_full_test(self, resume_ids, job_description_id):
        """
        运行完整测试流程
        
        Args:
            resume_ids: 简历ID列表
            job_description_id: 职位描述ID
        """
        print("=" * 70)
        print("批量简历修改功能测试")
        print("=" * 70)
        print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"API地址: {self.base_url}")
        print("=" * 70)
        
        # 1. 登录
        if not self.login():
            print("\n❌ 测试失败: 无法登录")
            return False
        
        # 2. 批量修改简历
        batch_id = self.test_batch_modify(resume_ids, job_description_id)
        if not batch_id:
            print("\n❌ 测试失败: 批量修改失败")
            return False
        
        # 3. 获取批量修改结果
        if not self.test_get_batch_results(batch_id):
            print("\n⚠️  警告: 无法获取批量修改结果")
        
        # 4. 获取历史记录
        if not self.test_get_history():
            print("\n⚠️  警告: 无法获取历史记录")
        
        print("\n" + "=" * 70)
        print("✅ 测试完成!")
        print("=" * 70)
        return True


def main():
    """主函数"""
    # 配置测试参数
    BASE_URL = "http://localhost:5000"  # 修改为你的API地址
    USERNAME = "test_user"  # 修改为你的测试用户名
    PASSWORD = "test_password"  # 修改为你的测试密码
    
    # 测试数据
    RESUME_IDS = [1, 2]  # 修改为实际存在的简历ID
    JOB_DESCRIPTION_ID = 1  # 修改为实际存在的职位描述ID
    
    print("\n⚙️  配置信息:")
    print(f"  API地址: {BASE_URL}")
    print(f"  用户名: {USERNAME}")
    print(f"  测试简历IDs: {RESUME_IDS}")
    print(f"  职位描述ID: {JOB_DESCRIPTION_ID}")
    print()
    
    # 创建测试器并运行测试
    tester = BatchModificationTester(BASE_URL, USERNAME, PASSWORD)
    success = tester.run_full_test(RESUME_IDS, JOB_DESCRIPTION_ID)
    
    if success:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print("\n💥 测试失败!")
        return 1


if __name__ == '__main__':
    exit(main())

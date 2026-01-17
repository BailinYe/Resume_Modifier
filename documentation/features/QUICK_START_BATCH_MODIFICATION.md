# 批量简历修改功能 - 快速入门指南
# Batch Resume Modification - Quick Start Guide

## 📋 功能简介

批量简历修改功能允许你一次性根据不同的职位描述修改多份简历，系统会智能地优化简历内容以提高与目标职位的匹配度。

## 🚀 快速开始

### 1. 安装数据库表

首先运行数据库迁移脚本以创建必要的表：

```bash
cd /srv/shared_folder/python/Resume_Modifier
python scripts/database/add_batch_modification_table.py
```

### 2. 准备数据

确保你的数据库中有：
- 至少一个用户账号
- 至少一份简历
- 至少一个职位描述

### 3. 使用API

#### 方法一: 使用cURL

```bash
# 1. 登录获取token
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'

# 保存返回的token
export TOKEN="your_token_here"

# 2. 批量修改简历
curl -X POST http://localhost:5000/api/resume/batch-modify \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_ids": [1, 2],
    "job_description_id": 1,
    "save_as_new": true
  }'

# 3. 查看修改历史
curl -X GET http://localhost:5000/api/resume/batch-modify/history \
  -H "Authorization: Bearer $TOKEN"
```

#### 方法二: 使用Python

```python
import requests

# 1. 登录
response = requests.post('http://localhost:5000/api/login', json={
    'username': 'your_username',
    'password': 'your_password'
})
token = response.json()['token']

# 2. 批量修改简历
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    'http://localhost:5000/api/resume/batch-modify',
    headers=headers,
    json={
        'resume_ids': [1, 2],
        'job_description_id': 1,
        'customization_options': {
            'optimize_summary': True,
            'optimize_experience': True,
            'optimize_skills': True,
            'optimize_projects': True
        },
        'save_as_new': True
    }
)

result = response.json()
print(f"批次ID: {result['batch_id']}")
print(f"成功修改: {result['results']['successful_modifications']} 份")
```

#### 方法三: 使用测试脚本

修改测试脚本中的配置：

```bash
# 编辑测试脚本
nano testing/test_batch_modification.py

# 修改以下变量:
BASE_URL = "http://localhost:5000"
USERNAME = "your_username"
PASSWORD = "your_password"
RESUME_IDS = [1, 2]  # 你的简历IDs
JOB_DESCRIPTION_ID = 1  # 你的职位描述ID

# 运行测试
python testing/test_batch_modification.py
```

## 📊 API端点一览

| 方法 | 端点 | 说明 |
|---|---|---|
| POST | `/api/resume/batch-modify` | 批量修改简历 |
| GET | `/api/resume/batch-modify/{batch_id}` | 获取批量修改结果 |
| GET | `/api/resume/batch-modify/history` | 获取批量修改历史 |

## 💡 使用建议

### 1. 选择合适的简历
- ✅ 选择与目标职位相关的简历
- ✅ 建议每次批量修改不超过5-10份简历
- ❌ 避免选择完全不相关的简历

### 2. 优化选项配置
```json
{
  "customization_options": {
    "optimize_summary": true,      // 优化个人简介
    "optimize_experience": true,   // 优化工作经验
    "optimize_skills": true,       // 优化技能列表
    "optimize_projects": true      // 优化项目经验
  }
}
```

### 3. 保存策略
- `"save_as_new": true` - 推荐！保留原简历，创建新版本
- `"save_as_new": false` - 覆盖原简历（谨慎使用）

## 🔍 查看结果

### 获取单个批次的详细结果

```bash
curl -X GET http://localhost:5000/api/resume/batch-modify/123 \
  -H "Authorization: Bearer $TOKEN"
```

返回内容包括：
- 每份简历的修改前后对比
- 匹配度评分
- 修改摘要
- 优化建议

### 查看所有历史记录

```bash
curl -X GET "http://localhost:5000/api/resume/batch-modify/history?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## 📈 示例输出

成功的批量修改会返回如下结果：

```json
{
  "success": true,
  "message": "Successfully modified 2 out of 2 resumes",
  "batch_id": 123,
  "results": {
    "job_description_title": "Senior Python Developer",
    "total_resumes": 2,
    "successful_modifications": 2,
    "failed_modifications": 0,
    "modified_resumes": [
      {
        "original_resume_id": 1,
        "original_title": "Software Engineer Resume",
        "modified_title": "Software Engineer Resume - Senior Python Developer Version",
        "match_score": 85,
        "modifications_summary": {
          "sections_modified": [
            "Professional Summary",
            "Skills",
            "Work Experience"
          ],
          "key_improvements": [
            "优化个人简介以匹配职位要求",
            "调整技能列表突出相关技能",
            "优化工作经验描述增强相关性"
          ]
        }
      }
    ]
  },
  "saved_resumes": [
    {
      "original_id": 1,
      "new_id": 3,
      "title": "Software Engineer Resume - Senior Python Developer Version"
    }
  ]
}
```

## ⚠️ 常见问题

### 问题1: "Job description not found"
**解决方案**: 确保职位描述ID存在且属于当前用户

```bash
# 查看用户的职位描述列表
curl -X GET http://localhost:5000/api/job_descriptions \
  -H "Authorization: Bearer $TOKEN"
```

### 问题2: "Resume not found"
**解决方案**: 确保简历ID存在且属于当前用户

```bash
# 查看用户的简历列表
curl -X GET http://localhost:5000/api/get_resume_list \
  -H "Authorization: Bearer $TOKEN"
```

### 问题3: 批量修改速度慢
**原因**: 每份简历需要调用AI服务进行分析和优化

**建议**:
- 分批处理大量简历
- 每批不超过5-10份
- 在非高峰时段进行

### 问题4: 某些简历修改失败
**查看错误信息**:

```python
result = response.json()
if result['results']['errors']:
    for error in result['results']['errors']:
        print(f"简历 {error['resume_id']}: {error['error']}")
```

## 🔧 故障排除

### 启用详细日志

在应用配置中启用调试模式：

```python
# config.py
DEBUG = True
LOG_LEVEL = 'DEBUG'
```

### 检查数据库连接

```bash
python -c "from app import create_app; app = create_app(); \
           from app.extensions import db; \
           with app.app_context(): print('DB OK' if db.engine.connect() else 'DB Failed')"
```

### 验证OpenAI API密钥

```bash
python -c "import os; from openai import OpenAI; \
           client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); \
           print('API Key OK')"
```

## 📚 更多资源

- 📖 [完整API文档](../api/API_DOCUMENTATION.md)
- 📖 [详细功能文档](./BATCH_RESUME_MODIFICATION.md)
- 🧪 [测试脚本](../../testing/test_batch_modification.py)
- 🗃️ [数据库迁移脚本](../../scripts/database/add_batch_modification_table.py)

## 💬 获取帮助

遇到问题？
1. 查看应用日志文件
2. 检查API响应中的错误信息
3. 参考完整文档
4. 使用测试脚本验证配置

## ✅ 检查清单

在使用批量修改功能前，请确认：

- [ ] 已运行数据库迁移脚本
- [ ] OpenAI API密钥已正确配置
- [ ] 数据库中有测试数据（用户、简历、职位描述）
- [ ] 能够成功登录获取token
- [ ] API端点可以正常访问

---

🎉 现在你可以开始使用批量简历修改功能了！

# 批量简历修改功能文档
# Batch Resume Modification Feature Documentation

## 功能概述 / Overview

批量简历修改功能允许用户根据不同的职位描述，一次性修改多份简历。系统会智能地分析每份简历与目标职位的匹配度，并自动优化简历内容以提高匹配度。

The batch resume modification feature allows users to modify multiple resumes at once based on different job descriptions. The system intelligently analyzes the match between each resume and target position, automatically optimizing resume content to improve the match score.

## 主要功能 / Key Features

### 1. 批量处理 / Batch Processing
- 一次性处理多份简历
- 并发处理提高效率
- 详细的处理结果追踪

### 2. 智能优化 / Intelligent Optimization
- **个人简介优化**: 根据职位要求重写个人简介
- **工作经验优化**: 调整工作经验描述，突出相关成就
- **技能列表优化**: 重新排序并添加相关技能
- **项目经验优化**: 优化项目描述以匹配职位要求

### 3. 匹配分析 / Match Analysis
- 简历与职位匹配度评分
- 详细的分析报告
- 改进建议

### 4. 历史记录 / History Tracking
- 保存所有批量修改记录
- 可查询历史修改结果
- 支持导出修改后的简历

## API端点 / API Endpoints

### 1. 批量修改简历 / Batch Modify Resumes

**端点 / Endpoint**: `POST /api/resume/batch-modify`

**认证 / Authentication**: 需要JWT Token (Bearer Token)

**请求体 / Request Body**:
```json
{
  "resume_ids": [1, 2, 3],
  "job_description_id": 1,
  "customization_options": {
    "optimize_summary": true,
    "optimize_experience": true,
    "optimize_skills": true,
    "optimize_projects": true
  },
  "save_as_new": true
}
```

**参数说明 / Parameters**:
- `resume_ids` (必需): 要修改的简历ID数组
- `job_description_id` (必需): 目标职位描述ID
- `customization_options` (可选): 自定义优化选项
  - `optimize_summary`: 是否优化个人简介 (默认: true)
  - `optimize_experience`: 是否优化工作经验 (默认: true)
  - `optimize_skills`: 是否优化技能列表 (默认: true)
  - `optimize_projects`: 是否优化项目经验 (默认: true)
- `save_as_new`: 是否保存为新简历 (默认: true)

**响应示例 / Response Example**:
```json
{
  "success": true,
  "message": "Successfully modified 3 out of 3 resumes",
  "batch_id": 123,
  "results": {
    "job_description_id": 1,
    "job_description_title": "Senior Software Engineer",
    "total_resumes": 3,
    "successful_modifications": 3,
    "failed_modifications": 0,
    "modified_resumes": [
      {
        "original_resume_id": 1,
        "original_title": "My Resume",
        "modified_title": "My Resume - Senior Software Engineer Version",
        "modified_content": { /* 完整的优化后简历数据 */ },
        "match_score": 85,
        "modifications_summary": {
          "sections_modified": ["Professional Summary", "Skills", "Work Experience"],
          "key_improvements": [
            "优化个人简介以匹配职位要求",
            "调整技能列表突出相关技能",
            "优化工作经验描述增强相关性"
          ]
        }
      }
    ],
    "errors": []
  },
  "saved_resumes": [
    {
      "original_id": 1,
      "new_id": 4,
      "title": "My Resume - Senior Software Engineer Version"
    }
  ]
}
```

### 2. 获取批量修改结果 / Get Batch Modification Results

**端点 / Endpoint**: `GET /api/resume/batch-modify/{batch_id}`

**认证 / Authentication**: 需要JWT Token

**响应示例 / Response Example**:
```json
{
  "success": true,
  "batch_id": 123,
  "user_id": 1,
  "job_description_id": 1,
  "job_title": "Senior Software Engineer",
  "status": "completed",
  "total_resumes": 3,
  "successful_modifications": 3,
  "failed_modifications": 0,
  "modified_resumes": [ /* 详细修改结果 */ ],
  "errors": [],
  "created_at": "2025-12-26T10:00:00",
  "completed_at": "2025-12-26T10:05:00"
}
```

### 3. 获取批量修改历史 / Get Batch Modification History

**端点 / Endpoint**: `GET /api/resume/batch-modify/history`

**认证 / Authentication**: 需要JWT Token

**查询参数 / Query Parameters**:
- `limit`: 返回记录数量 (默认: 20)
- `offset`: 跳过的记录数量，用于分页 (默认: 0)

**响应示例 / Response Example**:
```json
{
  "success": true,
  "total_count": 10,
  "limit": 20,
  "offset": 0,
  "batch_modifications": [
    {
      "batch_id": 123,
      "job_description_id": 1,
      "job_title": "Senior Software Engineer",
      "total_resumes": 3,
      "successful_modifications": 3,
      "failed_modifications": 0,
      "status": "completed",
      "created_at": "2025-12-26T10:00:00",
      "completed_at": "2025-12-26T10:05:00"
    }
  ]
}
```

## 使用示例 / Usage Examples

### Python示例 / Python Example

```python
import requests

# 1. 登录获取token
login_response = requests.post('http://api.example.com/api/login', json={
    'username': 'your_username',
    'password': 'your_password'
})
token = login_response.json()['token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# 2. 批量修改简历
batch_modify_data = {
    'resume_ids': [1, 2, 3],
    'job_description_id': 1,
    'customization_options': {
        'optimize_summary': True,
        'optimize_experience': True,
        'optimize_skills': True,
        'optimize_projects': True
    },
    'save_as_new': True
}

response = requests.post(
    'http://api.example.com/api/resume/batch-modify',
    headers=headers,
    json=batch_modify_data
)

result = response.json()
print(f"修改成功: {result['results']['successful_modifications']} 份简历")
print(f"批次ID: {result['batch_id']}")

# 3. 查询修改结果
batch_id = result['batch_id']
detail_response = requests.get(
    f'http://api.example.com/api/resume/batch-modify/{batch_id}',
    headers=headers
)

detail = detail_response.json()
for resume in detail['modified_resumes']:
    print(f"简历: {resume['modified_title']}")
    print(f"匹配分数: {resume['match_score']}")
    print(f"修改部分: {', '.join(resume['modifications_summary']['sections_modified'])}")
    print("---")

# 4. 查看历史记录
history_response = requests.get(
    'http://api.example.com/api/resume/batch-modify/history?limit=10',
    headers=headers
)

history = history_response.json()
print(f"总共 {history['total_count']} 条批量修改记录")
```

### JavaScript/Fetch示例 / JavaScript/Fetch Example

```javascript
// 1. 登录获取token
const login = async () => {
  const response = await fetch('http://api.example.com/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'your_username',
      password: 'your_password'
    })
  });
  const data = await response.json();
  return data.token;
};

// 2. 批量修改简历
const batchModifyResumes = async (token) => {
  const response = await fetch('http://api.example.com/api/resume/batch-modify', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      resume_ids: [1, 2, 3],
      job_description_id: 1,
      customization_options: {
        optimize_summary: true,
        optimize_experience: true,
        optimize_skills: true,
        optimize_projects: true
      },
      save_as_new: true
    })
  });
  
  const result = await response.json();
  console.log('修改成功:', result.results.successful_modifications, '份简历');
  console.log('批次ID:', result.batch_id);
  
  return result.batch_id;
};

// 3. 查询修改结果
const getBatchResults = async (token, batchId) => {
  const response = await fetch(
    `http://api.example.com/api/resume/batch-modify/${batchId}`,
    {
      headers: { 'Authorization': `Bearer ${token}` }
    }
  );
  
  const detail = await response.json();
  detail.modified_resumes.forEach(resume => {
    console.log('简历:', resume.modified_title);
    console.log('匹配分数:', resume.match_score);
    console.log('修改部分:', resume.modifications_summary.sections_modified.join(', '));
    console.log('---');
  });
};

// 使用示例
(async () => {
  const token = await login();
  const batchId = await batchModifyResumes(token);
  await getBatchResults(token, batchId);
})();
```

## 工作流程 / Workflow

1. **准备阶段 / Preparation**
   - 用户选择要修改的多份简历
   - 用户选择目标职位描述
   - 配置优化选项

2. **处理阶段 / Processing**
   - 系统逐一分析每份简历
   - 与职位描述进行匹配度分析
   - 使用AI优化简历内容

3. **生成阶段 / Generation**
   - 为每份简历生成优化版本
   - 计算匹配度评分
   - 生成修改摘要

4. **保存阶段 / Saving**
   - 将修改后的简历保存（可选择保存为新简历或覆盖原简历）
   - 记录批量修改历史
   - 返回详细结果

## 优化算法 / Optimization Algorithm

### 个人简介优化 / Professional Summary Optimization
- 提取职位描述中的关键要求
- 重写个人简介突出相关经验
- 使用职位描述中的关键词

### 工作经验优化 / Work Experience Optimization
- 使用行动导向的动词
- 添加可量化的成果
- 突出与目标职位相关的技能
- 调整描述以包含职位关键词

### 技能优化 / Skills Optimization
- 从职位描述中提取技术要求
- 按重要性重新排序技能
- 添加职位要求的相关技能

### 项目经验优化 / Projects Optimization
- 突出项目中使用的相关技术
- 强调项目成果和影响
- 使用职位描述中的技术词汇

## 数据库架构 / Database Schema

### BatchResumeModification表 / Table

| 字段 / Field | 类型 / Type | 说明 / Description |
|---|---|---|
| id | Integer | 主键 |
| user_id | Integer | 用户ID (外键) |
| job_description_id | Integer | 职位描述ID (外键) |
| job_title | String(200) | 职位标题 |
| total_resumes | Integer | 总简历数 |
| successful_modifications | Integer | 成功修改数 |
| failed_modifications | Integer | 失败修改数 |
| modification_results | JSON | 修改结果详情 |
| errors | JSON | 错误信息 |
| status | String(50) | 状态 (pending/in_progress/completed/failed) |
| created_at | DateTime | 创建时间 |
| completed_at | DateTime | 完成时间 |
| updated_at | DateTime | 更新时间 |

## 安装和配置 / Installation and Configuration

### 1. 数据库迁移 / Database Migration

运行以下脚本创建批量修改表:

```bash
cd /srv/shared_folder/python/Resume_Modifier
python scripts/database/add_batch_modification_table.py
```

### 2. 环境变量 / Environment Variables

确保配置了以下环境变量:

```bash
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
```

### 3. 依赖项 / Dependencies

确保安装了必要的Python包:

```bash
pip install flask sqlalchemy openai python-dotenv
```

## 性能优化 / Performance Optimization

### 批处理建议 / Batch Processing Recommendations
- 建议每批处理不超过10份简历
- 大批量任务可分批处理
- 使用异步处理提高效率

### AI调用优化 / AI Call Optimization
- 系统使用GPT-4o-mini模型平衡成本和质量
- 每份简历的处理时间约10-30秒
- 可根据需要调整temperature参数

## 错误处理 / Error Handling

系统会捕获并记录以下类型的错误:

1. **验证错误 / Validation Errors**
   - 无效的简历ID
   - 职位描述不存在
   - 参数格式错误

2. **处理错误 / Processing Errors**
   - AI服务调用失败
   - 数据格式错误
   - 网络超时

3. **数据库错误 / Database Errors**
   - 保存失败
   - 外键约束违反

所有错误都会被记录在`errors`字段中，不会影响其他简历的处理。

## 最佳实践 / Best Practices

1. **选择合适的简历 / Choose Appropriate Resumes**
   - 选择与目标职位相关的简历
   - 避免选择差异过大的简历

2. **优化选项配置 / Optimization Options**
   - 根据需要选择性开启优化选项
   - 对重要简历建议全面优化

3. **结果验证 / Result Verification**
   - 检查修改后的内容是否准确
   - 验证关键信息未被错误修改
   - 人工审核优化结果

4. **版本管理 / Version Management**
   - 建议保存为新简历以保留原版
   - 定期清理不需要的版本

## 限制和注意事项 / Limitations and Notes

1. **API调用限制 / API Rate Limits**
   - OpenAI API有调用频率限制
   - 大批量处理可能需要分批进行

2. **数据准确性 / Data Accuracy**
   - AI优化可能改变原意，需人工审核
   - 建议保留原始简历备份

3. **语言支持 / Language Support**
   - 当前主要支持中英文简历
   - 其他语言支持有限

4. **成本考虑 / Cost Considerations**
   - 每次批量修改会调用OpenAI API
   - 建议监控API使用量和成本

## 技术支持 / Technical Support

如遇到问题，请查看:
- 错误日志: 检查应用日志获取详细错误信息
- API文档: 访问 `/apidocs` 查看Swagger文档
- 数据库日志: 检查数据库查询日志

## 版本历史 / Version History

- **v1.0.0** (2025-12-26)
  - 初始版本发布
  - 支持基本的批量修改功能
  - 包含个人简介、工作经验、技能和项目优化
  - 提供完整的历史记录功能

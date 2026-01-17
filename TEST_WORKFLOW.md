# 批量改简历功能测试流程

## 📋 测试流程总结

### ✅ 已完成步骤

#### 1. 数据库准备
```bash
# 创建数据库
sudo -u postgres psql -c "CREATE DATABASE resume_app;"

# 创建数据库表
python create_db_tables.py
```

#### 2. 创建测试用户
```bash
# 运行用户创建脚本
python create_test_user.py

# 测试账号
Email: test@example.com
Password: password123
```

#### 3. 创建测试数据
```bash
# 运行测试数据创建脚本
python create_test_data.py

# 创建内容：
# - 1个默认简历模板
# - 1份测试简历（张三的软件工程师简历）
# - 3个职位描述（后端开发、全栈工程师、数据工程师）
```

#### 4. 运行完整测试
```bash
# 一键测试脚本
bash test_batch_modify.sh
```

---

## 🎯 测试的功能

### API 端点：`POST /api/resume/modify-for-jobs`

**功能**：一份简历根据多个职位描述生成优化版本

**请求参数**：
```json
{
  "resume_id": 1,                    // 基础简历ID
  "job_description_ids": [1, 2, 3],  // 目标职位ID列表
  "customization_options": {         // 可选：自定义优化选项
    "optimize_summary": true,
    "optimize_experience": true,
    "optimize_skills": true,
    "optimize_projects": true
  },
  "save_versions": true              // 是否自动保存为新简历
}
```

**返回结果**：
```json
{
  "success": true,
  "message": "Successfully generated 3 resume versions for 3 job positions",
  "results": {
    "original_resume_id": 1,
    "original_resume_title": "张三的软件工程师简历",
    "total_job_positions": 3,
    "successful_modifications": 3,
    "failed_modifications": 0,
    "modified_versions": [
      {
        "job_description_id": 1,
        "job_title": "后端开发工程师",
        "modified_title": "张三的软件工程师简历 - 后端开发工程师 Version",
        "saved_resume_id": 2,           // 新保存的简历ID
        "match_score": 85,              // 匹配分数
        "modified_content": {...},      // 优化后的简历内容
        "modifications_summary": {...}  // 修改摘要
      },
      // ... 其他职位版本
    ]
  }
}
```

---

## 📊 测试结果

### 成功生成的简历版本

| 原始简历 | 目标职位 | 新简历ID | 主要优化 |
|---------|---------|---------|---------|
| 张三的软件工程师简历 | 后端开发工程师 | 2 | Flask、PostgreSQL、RESTful API |
| 张三的软件工程师简历 | 全栈工程师 | 3 | JavaScript、React、MySQL |
| 张三的软件工程师简历 | 数据工程师 | 4 | SQL、Spark、Airflow、数据仓库 |

### 智能优化内容

每个版本都进行了以下优化：

1. **个人简介** - 根据职位要求重写专业摘要
2. **技能列表** - 智能添加/排序相关技能
3. **工作经验** - 优化描述突出相关经验
4. **项目描述** - 调整项目介绍匹配岗位

---

## 🚀 快速测试命令

### 方式一：使用测试脚本（推荐）
```bash
cd /srv/shared_folder/python/Resume_Modifier
bash test_batch_modify.sh
```

### 方式二：手动测试
```bash
# 1. 登录获取 Token
TOKEN=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}' \
  | jq -r '.token')

# 2. 测试批量修改API
curl -X POST http://localhost:5001/api/resume/modify-for-jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_ids": [1, 2, 3],
    "save_versions": true
  }' | jq .
```

---

## 📁 相关文件

### 测试脚本
- `create_db_tables.py` - 创建数据库表
- `create_test_user.py` - 创建测试用户
- `create_test_data.py` - 创建测试数据
- `test_batch_modify.sh` - 完整测试脚本

### 核心代码
- `core/app/server.py` - API端点定义
  - `/api/resume/modify-for-jobs` (新) - 一份简历多岗位
  - `/api/resume/batch-modify` (旧) - 多份简历一岗位
- `core/app/services/batch_resume_modifier.py` - 批量修改服务
  - `modify_resume_for_multiple_jobs()` - 新方法
  - `batch_modify_resumes()` - 原有方法

---

## 🔍 验证测试结果

### 检查生成的简历
```bash
# 查看用户的所有简历
curl -X GET "http://localhost:5001/api/get_resume_list" \
  -H "Authorization: Bearer $TOKEN" | jq .

# 查看特定简历详情
curl -X GET "http://localhost:5001/api/get_resume/2" \
  -H "Authorization: Bearer $TOKEN" | jq .
```

### 查看数据库记录
```bash
# 连接数据库
psql -U postgres -d resume_app

# 查看简历列表
SELECT user_id, serial_number, title FROM resumes;

# 查看职位描述
SELECT user_id, serial_number, title FROM job_descriptions;
```

---

## ✅ 测试通过标准

- [x] 数据库成功创建并初始化
- [x] 测试用户创建成功
- [x] 测试数据（简历、职位）创建成功
- [x] 登录API返回有效token
- [x] 批量修改API成功返回 `success: true`
- [x] 生成3个优化版本（对应3个职位）
- [x] 每个版本都保存为新简历（ID: 2, 3, 4）
- [x] 每个版本都包含优化后的内容
- [x] 优化内容符合目标职位要求

---

## 🎓 测试学到的内容

### 数据库要求
- User 表必须有 `username` 字段
- Resume 表必须有有效的 `template_id` 外键
- 密码必须使用 `set_password()` 方法哈希

### API设计
- **旧端点** `/api/resume/batch-modify`: 多简历 + 单职位
- **新端点** `/api/resume/modify-for-jobs`: 单简历 + 多职位 ⭐

### AI优化策略
- 使用 GPT-4o-mini 进行内容优化
- 针对不同职位智能调整技能、经验描述
- 保留原始内容结构，只优化文本
- 自动生成匹配度分析

---

## 📞 测试问题排查

### 问题1: 数据库连接失败
```
Error: database "resume_app" does not exist
```
**解决**: `sudo -u postgres psql -c "CREATE DATABASE resume_app;"`

### 问题2: 用户创建失败 - username null
```
Error: null value in column "username"
```
**解决**: 添加 `username='testuser'` 参数

### 问题3: 简历创建失败 - 外键约束
```
Error: foreign key constraint "resumes_template_id_fkey"
```
**解决**: 先创建 ResumeTemplate 记录

### 问题4: 登录失败 - 密码错误
```
Error: Invalid email or password
```
**解决**: 使用 `user.set_password('password123')` 而不是直接设置

---

## 🎯 下一步可以测试

1. **测试错误处理**
   - 无效的 resume_id
   - 无效的 job_description_ids
   - 用户权限验证

2. **测试边界情况**
   - 0个职位
   - 大量职位（10+）
   - save_versions=false

3. **性能测试**
   - 批量处理时间
   - 并发请求
   - 大型简历内容

4. **集成测试**
   - 与前端界面集成
   - 导出功能测试
   - Google Docs集成

---

## 📚 相关文档

- API文档: `/api/apidocs` (Swagger UI)
- 数据库Schema: `core/migrations/`
- 项目说明: `README.md`
- 配置说明: `configuration/environment/ENVIRONMENT_CONFIG.md`

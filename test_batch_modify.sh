#!/bin/bash
# 完整测试脚本 - 测试一份简历多岗位修改功能

echo "================================================"
echo "  测试一份简历多岗位修改功能"
echo "================================================"
echo ""

cd /srv/shared_folder/python/Resume_Modifier
source venv/bin/activate

# Step 1: 创建测试数据
echo "📝 Step 1: 创建测试数据..."
python create_test_data.py
echo ""

# Step 2: 登录获取 Token
echo "🔐 Step 2: 登录获取 Token..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:5001/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}')

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ 登录失败！"
    echo $LOGIN_RESPONSE | jq .
    exit 1
fi

echo "✅ 登录成功！Token: ${TOKEN:0:50}..."
echo ""

# Step 3: 测试新的API - 一份简历多岗位修改
echo "🚀 Step 3: 测试 /api/resume/modify-for-jobs ..."
echo "参数: resume_id=1, job_description_ids=[1,2,3]"
echo ""

MODIFY_RESPONSE=$(curl -s -X POST http://localhost:5001/api/resume/modify-for-jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_ids": [1, 2, 3],
    "customization_options": {
      "optimize_summary": true,
      "optimize_experience": true,
      "optimize_skills": true,
      "optimize_projects": true
    },
    "save_versions": true
  }')

echo "📊 响应结果："
echo $MODIFY_RESPONSE | jq .

# 检查是否成功
SUCCESS=$(echo $MODIFY_RESPONSE | jq -r '.success')
if [ "$SUCCESS" = "true" ]; then
    echo ""
    echo "✅✅✅ 测试成功！✅✅✅"
    echo ""
    
    # 显示生成的简历版本数量
    TOTAL_JOBS=$(echo $MODIFY_RESPONSE | jq -r '.results.total_job_positions')
    SUCCESSFUL=$(echo $MODIFY_RESPONSE | jq -r '.results.successful_modifications')
    echo "📈 统计："
    echo "  - 目标职位数: $TOTAL_JOBS"
    echo "  - 成功生成: $SUCCESSFUL 个简历版本"
    echo ""
    
    # 显示每个版本的详情
    echo "📋 生成的简历版本："
    echo $MODIFY_RESPONSE | jq -r '.results.modified_versions[] | "  - 职位: \(.job_title)\n    新简历ID: \(.saved_resume_id // "未保存")\n    匹配分数: \(.match_score)\n"'
else
    echo ""
    echo "❌ 测试失败！"
    ERROR=$(echo $MODIFY_RESPONSE | jq -r '.error')
    echo "错误信息: $ERROR"
fi

echo ""
echo "================================================"
echo "  测试完成"
echo "================================================"

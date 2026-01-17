#!/bin/bash
# 使用已有Token测试批量修改功能

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3Njg3MDQwMjV9.pPP43wcD9KCy_P3MIrN8KwsNJqAq7TKkqg80SADh9fw"

echo "================================================"
echo "  批量修改简历测试"
echo "================================================"
echo ""

# 检查简历和职位是否存在
echo "📋 Step 1: 检查现有数据..."
echo ""

echo "📝 你的简历列表："
curl -s -X GET "http://localhost:5001/api/get_resume_list" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.resumes[] | "ID: \(.serial_number) - \(.title)"'

echo ""
echo "💼 你的职位描述列表："
curl -s -X GET "http://localhost:5001/api/job-descriptions" \
  -H "Authorization: Bearer $TOKEN" | jq -r '.job_descriptions[]? | "ID: \(.serial_number) - \(.title)"' 2>/dev/null || echo "请先创建职位描述"

echo ""
echo "================================================"
echo ""

# 提示用户输入
read -p "请输入要修改的简历ID: " RESUME_ID
read -p "请输入职位描述ID列表（用空格分隔，如: 1 2 3）: " JOB_IDS

# 转换职位ID为JSON数组格式
JOB_IDS_ARRAY=$(echo $JOB_IDS | awk '{for(i=1;i<=NF;i++) printf "%s%d", (i>1?",":""), $i}')

echo ""
echo "🚀 开始批量修改..."
echo "简历ID: $RESUME_ID"
echo "职位ID: [$JOB_IDS_ARRAY]"
echo ""

# 调用API
RESPONSE=$(curl -s -X POST http://localhost:5001/api/resume/modify-for-jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"resume_id\": $RESUME_ID,
    \"job_description_ids\": [$JOB_IDS_ARRAY],
    \"customization_options\": {
      \"optimize_summary\": true,
      \"optimize_experience\": true,
      \"optimize_skills\": true,
      \"optimize_projects\": true
    },
    \"save_versions\": true
  }")

# 检查结果
SUCCESS=$(echo $RESPONSE | jq -r '.success')

if [ "$SUCCESS" = "true" ]; then
    echo "✅✅✅ 批量修改成功！✅✅✅"
    echo ""
    
    # 统计信息
    TOTAL=$(echo $RESPONSE | jq -r '.results.total_job_positions')
    SUCCESSFUL=$(echo $RESPONSE | jq -r '.results.successful_modifications')
    
    echo "📊 统计："
    echo "  - 目标职位数: $TOTAL"
    echo "  - 成功生成: $SUCCESSFUL 个简历版本"
    echo ""
    
    # 显示生成的版本
    echo "📋 生成的简历版本："
    echo $RESPONSE | jq -r '.results.modified_versions[] | "  ✓ \(.job_title)\n    新简历ID: \(.saved_resume_id)\n    匹配分数: \(.match_score)\n"'
    
    echo ""
    echo "💾 完整响应已保存到: batch_modify_result.json"
    echo $RESPONSE | jq . > batch_modify_result.json
    
else
    echo "❌ 批量修改失败！"
    echo ""
    ERROR=$(echo $RESPONSE | jq -r '.error')
    echo "错误信息: $ERROR"
    echo ""
    echo "完整响应:"
    echo $RESPONSE | jq .
fi

echo ""
echo "================================================"

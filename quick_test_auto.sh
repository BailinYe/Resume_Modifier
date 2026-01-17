#!/bin/bash
# 快速测试 - 自动使用现有数据

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3Njg3MDQwMjV9.pPP43wcD9KCy_P3MIrN8KwsNJqAq7TKkqg80SADh9fw"

echo "🚀 快速测试 - 一份简历多岗位修改"
echo ""

# 使用已知的测试数据: resume_id=1, job_ids=[1,2,3]
curl -X POST http://localhost:5001/api/resume/modify-for-jobs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_ids": [1, 2, 3],
    "save_versions": true
  }' | jq .

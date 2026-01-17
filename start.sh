#!/bin/bash

# Resume Modifier 快速启动脚本
# 用法: ./start.sh [dev|prod|docker]

set -e

echo "🚀 Resume Modifier 启动脚本"
echo "================================"

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查环境变量文件
if [ ! -f .env ]; then
    echo -e "${RED}❌ 错误: .env 文件不存在${NC}"
    echo -e "${YELLOW}💡 提示: 复制 .env.example 并配置:${NC}"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# 加载环境变量
export $(cat .env | grep -v '^#' | xargs)

# 获取启动模式
MODE=${1:-dev}

case $MODE in
    dev)
        echo -e "${GREEN}📍 启动模式: 开发环境${NC}"
        echo "================================"
        
        # 检查依赖
        if [ ! -d "venv" ]; then
            echo -e "${YELLOW}🔧 创建虚拟环境...${NC}"
            python3 -m venv venv
        fi
        
        echo -e "${YELLOW}🔧 激活虚拟环境...${NC}"
        source venv/bin/activate
        
        echo -e "${YELLOW}📦 安装依赖...${NC}"
        pip install -q -r core/requirements.txt
        
        echo -e "${YELLOW}🗄️ 检查数据库...${NC}"
        cd core
        flask db upgrade 2>/dev/null || echo "⚠️  数据库迁移跳过"
        cd ..
        
        echo -e "${GREEN}✅ 启动 Flask 开发服务器...${NC}"
        echo "📍 访问: http://localhost:5001"
        echo "📖 API文档: http://localhost:5001/apidocs"
        echo "================================"
        python wsgi.py
        ;;
    
    prod)
        echo -e "${GREEN}📍 启动模式: 生产环境 (Gunicorn)${NC}"
        echo "================================"
        
        # 检查 Gunicorn
        if ! command -v gunicorn &> /dev/null; then
            echo -e "${YELLOW}📦 安装 Gunicorn...${NC}"
            pip install gunicorn
        fi
        
        echo -e "${GREEN}✅ 启动 Gunicorn...${NC}"
        echo "📍 访问: http://localhost:5001"
        echo "👥 Workers: 4"
        echo "================================"
        gunicorn -w 4 -b 0.0.0.0:5001 --timeout 120 --access-logfile - wsgi:app
        ;;
    
    docker)
        echo -e "${GREEN}📍 启动模式: Docker Compose${NC}"
        echo "================================"
        
        # 检查 Docker
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}❌ 错误: Docker 未安装${NC}"
            exit 1
        fi
        
        echo -e "${YELLOW}🐳 构建并启动容器...${NC}"
        docker-compose up --build -d
        
        echo -e "${GREEN}✅ Docker 容器已启动${NC}"
        echo "📍 访问: http://localhost:5001"
        echo "📊 查看日志: docker-compose logs -f backend"
        echo "🛑 停止服务: docker-compose down"
        echo "================================"
        docker-compose logs -f backend
        ;;
    
    railway)
        echo -e "${GREEN}📍 启动模式: Railway 部署${NC}"
        echo "================================"
        python railway_start.py
        ;;
    
    *)
        echo -e "${RED}❌ 未知启动模式: $MODE${NC}"
        echo ""
        echo "用法: ./start.sh [dev|prod|docker|railway]"
        echo ""
        echo "模式说明:"
        echo "  dev      - 开发环境 (Flask 开发服务器)"
        echo "  prod     - 生产环境 (Gunicorn)"
        echo "  docker   - Docker Compose"
        echo "  railway  - Railway 部署脚本"
        exit 1
        ;;
esac

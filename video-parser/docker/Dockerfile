# 多阶段构建，减少最终镜像大小
FROM node:18-alpine AS frontend-build

# 设置工作目录
WORKDIR /app

# 复制前端项目文件
COPY spa-frontend/package*.json ./
RUN npm ci --only=production

# 复制前端源代码
COPY spa-frontend/ ./

# 构建前端
RUN npm run build

# 后端运行环境
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y     gcc     && rm -rf /var/lib/apt/lists/*

# 复制后端项目文件
COPY spa-backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端源代码
COPY spa-backend/ ./
COPY core/ ./core/

# 复制前端构建结果
COPY --from=frontend-build /app/dist ./static

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# 多平台视频链接解析与下载引擎

一个合规、可扩展、可维护的视频链接解析与下载系统。

## 功能特性

- 自动识别视频平台类型
- 解析视频元数据（标题、封面、分辨率、时长、编码）
- 在平台允许的前提下返回可下载的视频资源
- 优先返回无水印或官方高清源
- 不可下载时明确告知原因并给出替代方案
- 下载历史记录与数据分析
- AI助手集成（DeepSeek Chat和DeepSeek Reasoner）
- 作品文案写作功能
- 相关性分析功能

## 支持的平台

### 国内平台
- 哔哩哔哩（Bilibili）
- 抖音（Douyin）
- 快手（计划中）
- 小红书（计划中）
- 腾讯视频（计划中）
- 爱奇艺（计划中）

### 国际平台
- X / Twitter（计划中）
- YouTube（仅限公开视频、非 DRM）
- Vimeo（计划中）
- Dailymotion（计划中）

## 合规性

本工具严格遵守以下原则：
- 仅解析平台允许下载的公开视频内容
- 不支持付费、会员或受 DRM 保护的视频
- 尊重原平台版权与使用协议
- 所有下载行为需明确提示："仅限个人学习与平台允许范围内使用"

## 部署方式

本项目提供三种部署方式：

### 1. 网站手动部署版

适合小型项目或快速测试，将所有文件部署到Web服务器。

**部署步骤：**
1. 将`web-deploy`目录下的所有文件上传到Web服务器
2. 配置Web服务器（如Apache、Nginx）指向该目录
3. 确保Python环境和依赖已安装
4. 运行API服务

**依赖要求：**
- Python 3.7+
- Flask
- Requests

### 2. 前后端分离版

适合中大型项目，前端和后端分离部署，支持Vue和React两种前端框架。

**后端部署步骤：**
1. 安装Python依赖：`pip install -r requirements.txt`
2. 运行后端服务：`uvicorn main:app --host 0.0.0.0 --port 8000`

**前端部署步骤（Vue版本）：**
1. 安装Node.js依赖：`npm install`
2. 构建前端：`npm run build`
3. 将`dist`目录部署到Web服务器

**前端部署步骤（React版本）：**
1. 安装Node.js依赖：`npm install --package-lock-file package.react.json`
2. 构建前端：`npm run build --config vite.react.config.js`
3. 将`dist-react`目录部署到Web服务器

### 3. Docker快速部署版

适合需要快速部署和扩展的场景，使用Docker容器化部署。

**部署步骤：**
1. 确保已安装Docker和Docker Compose
2. 在`docker`目录下运行：`docker-compose up -d`
3. 服务将在http://localhost:8000（API）和http://localhost（前端）可用

## API文档

### 视频解析接口

**请求：**
```http
POST /api/parse
Content-Type: application/json

{
  "url": "https://www.bilibili.com/video/BV1xx411c7mD"
}
```

**响应：**
```json
{
  "success": true,
  "platform": "bilibili",
  "title": "视频标题",
  "cover": "https://...",
  "duration": 180,
  "streams": [
    {
      "quality": "1080p",
      "format": "mp4",
      "url": "https://...",
      "has_watermark": false
    }
  ],
  "downloadable": true,
  "disclaimer": "本工具仅解析平台允许下载的公开视频内容，请遵守原平台版权与使用协议"
}
```

### AI助手接口

**生成文本：**
```http
POST /api/ai/generate
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "prompt": "请为以下视频生成标题...",
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**视频内容分析：**
```http
POST /api/ai/analyze-video
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "title": "视频标题",
  "description": "视频描述",
  "platform": "bilibili"
}
```

**生成内容文案：**
```http
POST /api/ai/generate-content
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "video_data": {
    "title": "视频标题",
    "description": "视频描述"
  },
  "content_type": "title",
  "platform": "bilibili"
}
```

**相关性分析：**
```http
POST /api/ai/correlation-analysis
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "target": "分析目标内容",
  "analysis_type": "audience"
}
```

## 开发指南

### 添加新平台解析器

1. 在`core/parsers`目录下创建新的解析器文件
2. 继承`BasePlatformParser`类并实现必要方法
3. 在`core/parser.py`中注册新解析器

### 扩展AI功能

1. 在`api/ai_service.py`中添加新的AI服务方法
2. 在`api/routes.py`中添加新的API路由
3. 更新API文档

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](../LICENSE) 文件。

## 贡献指南

欢迎提交Issue和Pull Request来改进项目。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue：[项目Issues页面]
- 邮件：[项目邮箱]

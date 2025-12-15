# Multi-Platform Video Link Parser and Downloader

A compliant, scalable, and maintainable video link parsing and downloading system.

## Features

- Automatically identify video platform types
- Parse video metadata (title, cover, resolution, duration, encoding)
- Return downloadable video resources when permitted by the platform
- Prioritize watermark-free or official HD sources
- Clearly state reasons when download is not possible and provide alternatives
- Download history and data analysis
- AI assistant integration (DeepSeek Chat and DeepSeek Reasoner)
- Content copywriting features
- Correlation analysis functionality

## Supported Platforms

### Domestic Platforms
- Bilibili
- Douyin
- Kuaishou (Planned)
- Xiaohongshu (Planned)
- Tencent Video (Planned)
- iQIYI (Planned)

### International Platforms
- X / Twitter (Planned)
- YouTube (Public videos, non-DRM only)
- Vimeo (Planned)
- Dailymotion (Planned)

## Compliance

This tool strictly adheres to the following principles:
- Only parse publicly available video content permitted by platforms
- Do not support paid, membership, or DRM-protected videos
- Respect original platform copyright and terms of service
- All download behaviors must clearly state: "For personal learning and use within platform-permitted scope only"

## Deployment Methods

This project provides three deployment methods:

### 1. Web Manual Deployment

Suitable for small projects or quick testing, deploy all files to a web server.

**Deployment Steps:**
1. Upload all files from the `web-deploy` directory to your web server
2. Configure your web server (such as Apache, Nginx) to point to this directory
3. Ensure Python environment and dependencies are installed
4. Run the API service

**Dependency Requirements:**
- Python 3.7+
- Flask
- Requests

### 2. Frontend-Backend Separation

Suitable for medium to large projects, with separate frontend and backend deployment, supporting both Vue and React frontend frameworks.

**Backend Deployment Steps:**
1. Install Python dependencies: `pip install -r requirements.txt`
2. Run backend service: `uvicorn main:app --host 0.0.0.0 --port 8000`

**Frontend Deployment Steps (Vue Version):**
1. Install Node.js dependencies: `npm install`
2. Build frontend: `npm run build`
3. Deploy the `dist` directory to your web server

**Frontend Deployment Steps (React Version):**
1. Install Node.js dependencies: `npm install --package-lock-file package.react.json`
2. Build frontend: `npm run build --config vite.react.config.js`
3. Deploy the `dist-react` directory to your web server

### 3. Docker Quick Deployment

Suitable for scenarios requiring rapid deployment and scaling, using Docker containerized deployment.

**Deployment Steps:**
1. Ensure Docker and Docker Compose are installed
2. Run in the `docker` directory: `docker-compose up -d`
3. Services will be available at http://localhost:8000 (API) and http://localhost (frontend)

## API Documentation

### Video Parsing Interface

**Request:**
```http
POST /api/parse
Content-Type: application/json

{
  "url": "https://www.bilibili.com/video/BV1xx411c7mD"
}
```

**Response:**
```json
{
  "success": true,
  "platform": "bilibili",
  "title": "Video Title",
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
  "disclaimer": "This tool only parses publicly available video content permitted by platforms, please comply with original platform copyright and terms of service"
}
```

### AI Assistant Interface

**Generate Text:**
```http
POST /api/ai/generate
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "prompt": "Please generate a title for the following video...",
  "model": "deepseek-chat",
  "temperature": 0.7,
  "max_tokens": 2000
}
```

**Video Content Analysis:**
```http
POST /api/ai/analyze-video
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "title": "Video Title",
  "description": "Video Description",
  "platform": "bilibili"
}
```

**Generate Content Copy:**
```http
POST /api/ai/generate-content
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "video_data": {
    "title": "Video Title",
    "description": "Video Description"
  },
  "content_type": "title",
  "platform": "bilibili"
}
```

**Correlation Analysis:**
```http
POST /api/ai/correlation-analysis
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "target": "Target content for analysis",
  "analysis_type": "audience"
}
```

## Development Guide

### Adding New Platform Parsers

1. Create a new parser file in the `core/parsers` directory
2. Inherit from the `BasePlatformParser` class and implement necessary methods
3. Register the new parser in `core/parser.py`

### Extending AI Features

1. Add new AI service methods in `api/ai_service.py`
2. Add new API routes in `api/routes.py`
3. Update API documentation

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Contributing Guidelines

Issues and Pull Requests are welcome to improve the project.

## Contact

For questions or suggestions, please contact through:
- Submit Issues: [Project Issues Page]
- Email: [Project Email]

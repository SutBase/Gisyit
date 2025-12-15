# -*- coding: utf-8 -*-
"""
视频解析API服务 - 前后端分离版
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
from typing import Dict, Any, List, Optional
import os

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 导入核心解析器
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.parser import parse_video_url, PlatformType

# 导入API路由
from api.routes import router as api_router

app = FastAPI(
    title="多平台视频链接解析与下载引擎 API",
    description="合规、可扩展、可维护的视频链接解析与下载系统",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的允许来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 包含API路由
app.include_router(api_router, prefix="/api", tags=["API"])

# 定义请求模型
class ParseRequest(BaseModel):
    url: str

# 定义响应模型
class StreamInfo(BaseModel):
    quality: str
    format: str
    url: str
    has_watermark: bool
    size: Optional[int] = None
    duration: Optional[int] = None

class ParseResponse(BaseModel):
    success: bool
    platform: Optional[str] = None
    title: Optional[str] = None
    cover: Optional[str] = None
    duration: Optional[int] = None
    streams: Optional[List[StreamInfo]] = None
    downloadable: Optional[bool] = None
    reason: Optional[str] = None
    disclaimer: Optional[str] = None

class PlatformInfo(BaseModel):
    id: str
    name: str
    enabled: bool

class PlatformsResponse(BaseModel):
    success: bool
    platforms: List[PlatformInfo]

@app.post("/api/parse", response_model=ParseResponse)
async def parse_video(request: ParseRequest):
    """解析视频API接口"""
    try:
        url = request.url
        if not url:
            raise HTTPException(status_code=400, detail="URL cannot be empty")

        # 解析视频
        logger.info(f"解析视频URL: {url}")
        result = parse_video_url(url)

        # 添加免责声明
        if result.get('success') and result.get('downloadable'):
            result['disclaimer'] = "本工具仅解析平台允许下载的公开视频内容，请遵守原平台版权与使用协议"

        return result

    except Exception as e:
        logger.error(f"解析视频时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/platforms", response_model=PlatformsResponse)
async def get_supported_platforms():
    """获取支持的平台列表"""
    platforms = [
        {
            'id': 'bilibili',
            'name': '哔哩哔哩',
            'enabled': True
        },
        {
            'id': 'douyin',
            'name': '抖音',
            'enabled': True
        },
        {
            'id': 'kuaishou',
            'name': '快手',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'xiaohongshu',
            'name': '小红书',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'tencent_video',
            'name': '腾讯视频',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'iqiyi',
            'name': '爱奇艺',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'twitter',
            'name': 'Twitter/X',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'youtube',
            'name': 'YouTube',
            'enabled': True
        },
        {
            'id': 'vimeo',
            'name': 'Vimeo',
            'enabled': False  # 示例中未实现
        },
        {
            'id': 'dailymotion',
            'name': 'Dailymotion',
            'enabled': False  # 示例中未实现
        }
    ]

    return {
        'success': True,
        'platforms': platforms
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        'status': 'ok',
        'message': 'Video Parser API is running'
    }

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'success': False,
            'error': exc.detail
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            'success': False,
            'error': "Internal server error"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

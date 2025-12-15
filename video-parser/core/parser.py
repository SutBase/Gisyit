# -*- coding: utf-8 -*-
"""
多平台视频链接解析与下载引擎 - 核心解析器
"""

import re
import json
import urllib.parse
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from enum import Enum


class PlatformType(Enum):
    """支持的视频平台枚举"""
    BILIBILI = "bilibili"
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    XIAOHONGSHU = "xiaohongshu"
    TENCENT_VIDEO = "tencent_video"
    IQIYI = "iqiyi"
    TWITTER = "twitter"
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    DAILYMOTION = "dailymotion"
    UNKNOWN = "unknown"


@dataclass
class VideoStream:
    """视频流信息"""
    quality: str  # 分辨率，如 "1080p"
    format: str   # 格式，如 "mp4"
    url: str      # 下载链接
    has_watermark: bool  # 是否有水印
    size: Optional[int] = None  # 文件大小（字节）
    duration: Optional[int] = None  # 时长（秒）


@dataclass
class VideoMetadata:
    """视频元数据"""
    platform: PlatformType
    title: str
    cover: str
    duration: int  # 秒
    streams: List[VideoStream]
    downloadable: bool
    reason: Optional[str] = None  # 不可下载时的原因


class BasePlatformParser(ABC):
    """平台解析器基类"""

    @property
    @abstractmethod
    def platform_type(self) -> PlatformType:
        """返回该解析器对应的平台类型"""
        pass

    @abstractmethod
    def match(self, url: str) -> bool:
        """判断URL是否属于该平台"""
        pass

    @abstractmethod
    def normalize_url(self, url: str) -> str:
        """标准化URL，处理短链接、重定向等"""
        pass

    @abstractmethod
    def parse(self, url: str) -> VideoMetadata:
        """解析视频URL，返回元数据"""
        pass


class VideoParserEngine:
    """视频解析引擎主类"""

    def __init__(self):
        self.parsers: List[BasePlatformParser] = []
        self._register_default_parsers()

    def _register_default_parsers(self):
        """注册默认的平台解析器"""
        from .parsers import BilibiliParser, DouyinParser, YouTubeParser
        self.parsers.extend([
            BilibiliParser(),
            DouyinParser(),
            YouTubeParser()
        ])

    def register_parser(self, parser: BasePlatformParser):
        """注册新的平台解析器"""
        self.parsers.append(parser)

    def detect_platform(self, url: str) -> PlatformType:
        """检测视频链接所属平台"""
        for parser in self.parsers:
            if parser.match(url):
                return parser.platform_type
        return PlatformType.UNKNOWN

    def normalize_url(self, url: str) -> str:
        """标准化URL"""
        platform = self.detect_platform(url)
        for parser in self.parsers:
            if parser.platform_type == platform:
                return parser.normalize_url(url)
        return url

    def parse_video(self, url: str) -> Union[VideoMetadata, Dict[str, str]]:
        """解析视频链接"""
        platform = self.detect_platform(url)

        if platform == PlatformType.UNKNOWN:
            return {
                "success": False,
                "reason": "Unsupported video platform or invalid URL"
            }

        for parser in self.parsers:
            if parser.platform_type == platform:
                try:
                    normalized_url = self.normalize_url(url)
                    metadata = parser.parse(normalized_url)
                    return metadata
                except Exception as e:
                    return {
                        "success": False,
                        "reason": f"Failed to parse video: {str(e)}"
                    }

        return {
            "success": False,
            "reason": "No parser available for this platform"
        }

    def to_dict(self, data: Union[VideoMetadata, Dict]) -> Dict:
        """将解析结果转换为字典格式"""
        if isinstance(data, dict):
            return data

        return {
            "success": True,
            "platform": data.platform.value,
            "title": data.title,
            "cover": data.cover,
            "duration": data.duration,
            "streams": [
                {
                    "quality": stream.quality,
                    "format": stream.format,
                    "url": stream.url,
                    "has_watermark": stream.has_watermark,
                    "size": stream.size,
                    "duration": stream.duration
                }
                for stream in data.streams
            ],
            "downloadable": data.downloadable,
            "reason": data.reason
        }


# 单例模式，确保全局只有一个解析引擎实例
_parser_engine = None


def get_parser_engine() -> VideoParserEngine:
    """获取全局解析引擎实例"""
    global _parser_engine
    if _parser_engine is None:
        _parser_engine = VideoParserEngine()
    return _parser_engine


def parse_video_url(url: str) -> Dict:
    """便捷函数：解析视频URL并返回JSON格式的结果"""
    engine = get_parser_engine()
    result = engine.parse_video(url)
    return engine.to_dict(result)

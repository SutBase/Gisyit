# -*- coding: utf-8 -*-
"""
YouTube视频解析器
"""

import re
import json
import requests
from typing import List
from urllib.parse import urlparse, parse_qs

from ..parser import BasePlatformParser, PlatformType, VideoMetadata, VideoStream


class YouTubeParser(BasePlatformParser):
    """YouTube视频解析器"""

    @property
    def platform_type(self) -> PlatformType:
        return PlatformType.YOUTUBE

    def match(self, url: str) -> bool:
        """判断URL是否属于YouTube"""
        patterns = [
            r'youtube\.com/watch\?v=[a-zA-Z0-9_-]+',
            r'youtu\.be/[a-zA-Z0-9_-]+',
            r'youtube\.com/embed/[a-zA-Z0-9_-]+',
            r'youtube\.com/v/[a-zA-Z0-9_-]+',
            r'youtube\.com/shorts/[a-zA-Z0-9_-]+',
        ]
        return any(re.search(pattern, url) for pattern in patterns)

    def normalize_url(self, url: str) -> str:
        """标准化URL，处理短链接、重定向等"""
        # 处理短链接
        if 'youtu.be' in url:
            video_id = self._extract_video_id(url)
            if video_id:
                return f'https://www.youtube.com/watch?v={video_id}'

        # 处理embed链接
        if 'youtube.com/embed/' in url:
            video_id = self._extract_video_id(url)
            if video_id:
                return f'https://www.youtube.com/watch?v={video_id}'

        # 处理shorts链接
        if 'youtube.com/shorts/' in url:
            video_id = self._extract_video_id(url)
            if video_id:
                return f'https://www.youtube.com/watch?v={video_id}'

        # 确保URL是完整的
        if not url.startswith('http'):
            url = 'https://' + url

        return url

    def _extract_video_id(self, url: str) -> str:
        """从URL中提取视频ID"""
        # 标准格式
        if 'youtube.com/watch' in url:
            parsed = urlparse(url)
            query = parse_qs(parsed.query)
            return query.get('v', [''])[0]

        # 短链接格式
        if 'youtu.be' in url:
            path = urlparse(url).path
            return path.lstrip('/')

        # embed格式
        if 'youtube.com/embed/' in url:
            match = re.search(r'/embed/([a-zA-Z0-9_-]+)', url)
            if match:
                return match.group(1)

        # shorts格式
        if 'youtube.com/shorts/' in url:
            match = re.search(r'/shorts/([a-zA-Z0-9_-]+)', url)
            if match:
                return match.group(1)

        return ""

    def _get_video_info(self, video_id: str) -> dict:
        """获取视频基本信息"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 使用YouTube Data API v3
        api_url = f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json'

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                'title': data.get('title', ''),
                'author_name': data.get('author_name', ''),
                'author_url': data.get('author_url', ''),
                'thumbnail_url': data.get('thumbnail_url', ''),
            }
        except Exception:
            # 如果oembed API失败，尝试从页面解析
            return self._parse_video_page(video_id)

    def _parse_video_page(self, video_id: str) -> dict:
        """从视频页面解析信息"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        page_url = f'https://www.youtube.com/watch?v={video_id}'

        try:
            response = requests.get(page_url, headers=headers, timeout=10)
            response.raise_for_status()
            html = response.text

            # 提取标题
            title_match = re.search(r'"title":"([^"]+)"', html)
            title = title_match.group(1) if title_match else ""

            # 提取缩略图
            thumbnail_match = re.search(r'"thumbnailUrl":"([^"]+)"', html)
            thumbnail = thumbnail_match.group(1) if thumbnail_match else ""

            # 提取时长
            duration_match = re.search(r'"lengthSeconds":"(\d+)"', html)
            duration = int(duration_match.group(1)) if duration_match else 0

            return {
                'title': title,
                'thumbnail_url': thumbnail,
                'duration': duration
            }
        except Exception as e:
            raise Exception(f"解析视频页面失败: {str(e)}")

    def _get_video_streams(self, video_id: str) -> List[VideoStream]:
        """获取视频流信息"""
        # 注意：在实际应用中，这里可以使用yt-dlp或youtube-dl等工具获取视频流
        # 但由于合规性考虑，这里只返回一个示例实现

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # 这里仅作为示例，实际应用中可能需要使用yt-dlp等工具
        # 返回空列表表示无法直接下载
        return []

    def parse(self, url: str) -> VideoMetadata:
        """解析YouTube视频"""
        try:
            # 提取视频ID
            video_id = self._extract_video_id(url)
            if not video_id:
                raise Exception("无法从URL中提取视频ID")

            # 获取视频基本信息
            video_info = self._get_video_info(video_id)
            if not video_info:
                raise Exception("获取视频信息失败")

            title = video_info.get('title', '')
            cover = video_info.get('thumbnail_url', '')
            duration = video_info.get('duration', 0)

            # 获取视频流
            streams = self._get_video_streams(video_id)

            # 检查视频是否可下载
            if not streams:
                return VideoMetadata(
                    platform=self.platform_type,
                    title=title,
                    cover=cover,
                    duration=duration,
                    streams=[],
                    downloadable=False,
                    reason="YouTube视频受版权保护，无法直接下载。请使用YouTube Premium或第三方工具下载。"
                )

            return VideoMetadata(
                platform=self.platform_type,
                title=title,
                cover=cover,
                duration=duration,
                streams=streams,
                downloadable=len(streams) > 0
            )
        except Exception as e:
            return VideoMetadata(
                platform=self.platform_type,
                title="",
                cover="",
                duration=0,
                streams=[],
                downloadable=False,
                reason=f"解析失败: {str(e)}"
            )

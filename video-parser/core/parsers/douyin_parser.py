# -*- coding: utf-8 -*-
"""
抖音视频解析器
"""

import re
import json
import requests
from typing import List
from urllib.parse import urlparse, parse_qs

from ..parser import BasePlatformParser, PlatformType, VideoMetadata, VideoStream


class DouyinParser(BasePlatformParser):
    """抖音视频解析器"""

    @property
    def platform_type(self) -> PlatformType:
        return PlatformType.DOUYIN

    def match(self, url: str) -> bool:
        """判断URL是否属于抖音"""
        patterns = [
            r'v\.douyin\.com/[a-zA-Z0-9]+',
            r'douyin\.com/video/[a-zA-Z0-9]+',
            r'www\.iesdouyin\.com/share/video/[a-zA-Z0-9]+',
            r'www\.douyin\.com/user/[a-zA-Z0-9]+',  # 用户页面，可能包含视频
        ]
        return any(re.search(pattern, url) for pattern in patterns)

    def normalize_url(self, url: str) -> str:
        """标准化URL，处理短链接、重定向等"""
        # 处理短链接
        if 'v.douyin.com' in url:
            try:
                response = requests.head(url, allow_redirects=True, timeout=10)
                return response.url
            except Exception:
                return url

        # 确保URL是完整的
        if not url.startswith('http'):
            url = 'https://' + url

        return url

    def _extract_video_id(self, url: str) -> str:
        """从URL中提取视频ID"""
        # 从分享链接中提取
        video_match = re.search(r'/video/([a-zA-Z0-9]+)', url)
        if video_match:
            return video_match.group(1)

        # 从用户页面URL中提取
        user_match = re.search(r'/user/([a-zA-Z0-9]+)', url)
        if user_match:
            # 用户页面需要进一步处理，这里暂时返回空
            return ""

        return ""

    def _get_video_info(self, video_id: str) -> dict:
        """获取视频基本信息"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.douyin.com'
        }

        api_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}'

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get('item_list'):
                raise Exception("未找到视频信息")

            return data.get('item_list', [])[0]
        except Exception as e:
            raise Exception(f"获取视频信息失败: {str(e)}")

    def _get_video_streams(self, video_info: dict) -> List[VideoStream]:
        """获取视频流信息"""
        streams = []

        try:
            # 获取视频地址
            video = video_info.get('video', {})
            play_addr = video.get('play_addr', {})

            if not play_addr or not play_addr.get('url_list'):
                return streams

            # 获取不同清晰度的视频
            for i, url in enumerate(play_addr.get('url_list', [])):
                # 抖音视频通常有水印，但官方API可能提供无水印版本
                # 这里假设获取的是无水印版本
                quality = "原画"

                streams.append(VideoStream(
                    quality=quality,
                    format="mp4",
                    url=url,
                    has_watermark=False,  # 假设是无水印版本
                    size=video.get('size'),
                    duration=video_info.get('duration')
                ))

            # 如果有高清版本
            download_addr = video.get('download_addr', {})
            if download_addr and download_addr.get('url_list'):
                for url in download_addr.get('url_list', []):
                    streams.append(VideoStream(
                        quality="高清",
                        format="mp4",
                        url=url,
                        has_watermark=True,  # 下载版本可能有水印
                        size=video.get('size'),
                        duration=video_info.get('duration')
                    ))

            return streams
        except Exception as e:
            raise Exception(f"获取视频流失败: {str(e)}")

    def parse(self, url: str) -> VideoMetadata:
        """解析抖音视频"""
        try:
            # 提取视频ID
            video_id = self._extract_video_id(url)
            if not video_id:
                raise Exception("无法从URL中提取视频ID")

            # 获取视频基本信息
            video_info = self._get_video_info(video_id)
            if not video_info:
                raise Exception("获取视频信息失败")

            # 提取视频信息
            desc = video_info.get('desc', '')
            cover = ""
            duration = video_info.get('duration', 0)

            # 获取封面
            video = video_info.get('video', {})
            if video and video.get('cover', {}).get('url_list'):
                cover = video.get('cover', {}).get('url_list', [])[0]

            # 获取视频流
            streams = self._get_video_streams(video_info)

            # 检查视频是否可下载
            if video_info.get('status', {}).get('is_delete', False):
                return VideoMetadata(
                    platform=self.platform_type,
                    title=desc,
                    cover=cover,
                    duration=duration,
                    streams=[],
                    downloadable=False,
                    reason="视频已被删除"
                )

            return VideoMetadata(
                platform=self.platform_type,
                title=desc,
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

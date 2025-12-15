# -*- coding: utf-8 -*-
"""
哔哩哔哩视频解析器
"""

import re
import json
import requests
from typing import List
from urllib.parse import urlparse, parse_qs

from ..parser import BasePlatformParser, PlatformType, VideoMetadata, VideoStream


class BilibiliParser(BasePlatformParser):
    """哔哩哔哩视频解析器"""

    @property
    def platform_type(self) -> PlatformType:
        return PlatformType.BILIBILI

    def match(self, url: str) -> bool:
        """判断URL是否属于哔哩哔哩"""
        patterns = [
            r'bilibili\.com/video/[bB][vV][a-zA-Z0-9]+',
            r'bilibili\.com/video/av\d+',
            r'b23\.tv/[a-zA-Z0-9]+',  # 短链接
            r'bilibili\.com/medialist/detail/ml\d+',  # 播单
        ]
        return any(re.search(pattern, url) for pattern in patterns)

    def normalize_url(self, url: str) -> str:
        """标准化URL，处理短链接、重定向等"""
        # 处理短链接
        if 'b23.tv' in url:
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
        # BV号
        bv_match = re.search(r'/video/([bB][vV][a-zA-Z0-9]+)', url)
        if bv_match:
            return bv_match.group(1)

        # AV号
        av_match = re.search(r'/video/av(\d+)', url)
        if av_match:
            return av_match.group(1)

        return ""

    def _get_video_info(self, video_id: str) -> dict:
        """获取视频基本信息"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com'
        }

        # 判断是BV号还是AV号
        if video_id.lower().startswith('bv'):
            api_url = f'https://api.bilibili.com/x/web-interface/view?bvid={video_id}'
        else:
            api_url = f'https://api.bilibili.com/x/web-interface/view?aid={video_id}'

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('code') != 0:
                raise Exception(f"API error: {data.get('message')}")

            return data.get('data', {})
        except Exception as e:
            raise Exception(f"Failed to get video info: {str(e)}")

    def _get_video_streams(self, video_id: str, cid: int) -> List[VideoStream]:
        """获取视频流信息"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com'
        }

        api_url = f'https://api.bilibili.com/x/player/playurl?bvid={video_id}&cid={cid}&qn=80&fnver=0&fnval=16&fourk=1'

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('code') != 0:
                raise Exception(f"API error: {data.get('message')}")

            playurl_data = data.get('data', {})
            streams = []

            # 解析不同清晰度的视频流
            if 'dash' in playurl_data:
                # DASH格式
                for video in playurl_data['dash'].get('video', []):
                    quality_map = {
                        120: "8K",
                        116: "1080P60",
                        112: "1080P+",
                        80: "1080P",
                        74: "720P60",
                        64: "720P",
                        32: "480P",
                        16: "360P"
                    }
                    quality = quality_map.get(video.get('id'), f"Quality_{video.get('id')}")

                    streams.append(VideoStream(
                        quality=quality,
                        format=video.get('codecs', 'unknown'),
                        url=video.get('baseUrl', ''),
                        has_watermark=False,  # B站官方流通常无水印
                        size=video.get('bandwidth'),
                        duration=video.get('duration')
                    ))
            else:
                # 传统格式
                durl = playurl_data.get('durl', [])
                if durl:
                    quality_map = {
                        80: "1080P",
                        64: "720P",
                        32: "480P",
                        16: "360P"
                    }
                    quality = quality_map.get(playurl_data.get('quality', 16), "Unknown")

                    streams.append(VideoStream(
                        quality=quality,
                        format="mp4",
                        url=durl[0].get('url', ''),
                        has_watermark=False,
                        size=durl[0].get('size'),
                        duration=durl[0].get('length')
                    ))

            return streams
        except Exception as e:
            raise Exception(f"Failed to get video streams: {str(e)}")

    def parse(self, url: str) -> VideoMetadata:
        """解析哔哩哔哩视频"""
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
            cover = video_info.get('pic', '')
            duration = video_info.get('duration', 0)
            cid = video_info.get('cid', 0)

            # 检查视频是否可下载
            if video_info.get('redirect_url'):
                return VideoMetadata(
                    platform=self.platform_type,
                    title=title,
                    cover=cover,
                    duration=duration,
                    streams=[],
                    downloadable=False,
                    reason="此视频需要登录或会员才能观看"
                )

            # 获取视频流
            streams = self._get_video_streams(video_id, cid)

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

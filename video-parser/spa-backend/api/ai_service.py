# -*- coding: utf-8 -*-
"""
AI服务模块
"""

import os
import httpx
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel
from fastapi import HTTPException, status
import time
from .keys import key_manager

class AIRequest(BaseModel):
    """AI请求模型"""
    prompt: str
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 2000

class AIResponse(BaseModel):
    """AI响应模型"""
    content: str
    model: str
    usage: Dict[str, int]

class AIService:
    """AI服务类"""

    def __init__(self):
        self.base_url = "https://api.deepseek.com/v1/chat/completions"

    async def generate_text(self, request: AIRequest, api_key_name: str = "default") -> AIResponse:
        """生成文本"""
        # 获取API密钥
        api_key_obj = key_manager.get_key(api_key_name)
        if not api_key_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"API密钥 '{api_key_name}' 不存在或已失效"
            )

        # 准备请求数据
        data = {
            "model": request.model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个专业的视频内容分析师和文案写作助手，擅长分析视频内容、撰写吸引人的文案和提供有价值的建议。"
                },
                {
                    "role": "user",
                    "content": request.prompt
                }
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key_obj.key}"
        }

        # 发送请求
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.base_url,
                    json=data,
                    headers=headers
                )
                response.raise_for_status()

                result = response.json()

                return AIResponse(
                    content=result["choices"][0]["message"]["content"],
                    model=result["model"],
                    usage=result.get("usage", {})
                )
        except httpx.HTTPStatusError as e:
            error_detail = "API请求失败"
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", error_detail)
            except:
                pass

            raise HTTPException(
                status_code=e.response.status_code,
                detail=error_detail
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"生成文本时发生错误: {str(e)}"
            )

    async def analyze_video_content(self, video_data: Dict[str, Any], api_key_name: str = "default") -> Dict[str, Any]:
        """分析视频内容"""
        # 构建分析提示
        prompt = f"""请分析以下视频内容，提供详细的分析报告：

视频标题：{video_data.get('title', '')}
视频平台：{video_data.get('platform', '')}
视频时长：{video_data.get('duration', 0)}秒
视频描述：{video_data.get('description', '')}

请从以下几个方面进行分析：
1. 内容主题和类别
2. 目标受众特征（年龄、性别、兴趣等）
3. 内容质量和吸引力评估
4. 优化建议（标题、描述、标签等）
5. 潜在传播力和热度预测

请以JSON格式返回分析结果，包含上述所有方面。"""

        # 调用AI生成分析结果
        response = await self.generate_text(
            AIRequest(prompt=prompt, model="deepseek-reasoner"),
            api_key_name=api_key_name
        )

        # 尝试解析JSON结果
        try:
            # 查找JSON部分
            content = response.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
        except:
            pass

        # 如果无法解析JSON，返回原始内容
        return {
            "analysis": response.content,
            "model": response.model,
            "usage": response.usage
        }

    async def generate_content_copy(self, video_data: Dict[str, Any], content_type: str, 
                               platform: str = None, api_key_name: str = "default") -> Dict[str, Any]:
        """生成内容文案"""
        # 构建文案生成提示
        platform_text = f"针对{platform}平台" if platform else ""

        if content_type == "title":
            prompt = f"""请为以下视频{platform_text}生成5个吸引人的标题建议：

视频标题：{video_data.get('title', '')}
视频描述：{video_data.get('description', '')}

要求：
1. 每个标题不超过30字
2. 符合{platform_text if platform else "视频平台"}的用户喜好
3. 具有吸引力和点击率潜力

请直接返回5个标题，每行一个。"""

        elif content_type == "description":
            prompt = f"""请为以下视频{platform_text}生成一段吸引人的描述：

视频标题：{video_data.get('title', '')}
视频描述：{video_data.get('description', '')}

要求：
1. 描述不超过200字
2. 突出视频亮点和价值
3. 符合{platform_text if platform else "视频平台"}的风格
4. 包含适当的表情符号

请直接返回生成的描述。"""

        elif content_type == "tags":
            prompt = f"""请为以下视频{platform_text}推荐10个相关标签：

视频标题：{video_data.get('title', '')}
视频描述：{video_data.get('description', '')}

要求：
1. 每个标签不超过10字
2. 涵盖视频的主要内容和特点
3. 包含热门和长尾关键词
4. 符合{platform_text if platform else "视频平台"}的标签规范

请直接返回10个标签，用逗号分隔。"""

        elif content_type == "full":
            prompt = f"""请为以下视频{platform_text}生成完整的文案，包括标题、描述和标签：

视频标题：{video_data.get('title', '')}
视频描述：{video_data.get('description', '')}

要求：
1. 提供3个标题选项（每个不超过30字）
2. 提供一段描述（不超过200字）
3. 提供10个相关标签（每个不超过10字）
4. 整体风格符合{platform_text if platform else "视频平台"}
5. 具有吸引力和传播潜力

请以JSON格式返回结果，包含titles、description和tags三个字段。"""

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的内容类型: {content_type}"
            )

        # 调用AI生成文案
        response = await self.generate_text(
            AIRequest(prompt=prompt, model="deepseek-chat"),
            api_key_name=api_key_name
        )

        # 尝试解析结构化结果
        if content_type == "full":
            try:
                # 查找JSON部分
                content = response.content
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1

                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
            except:
                pass

        # 返回结果
        return {
            "content": response.content,
            "type": content_type,
            "platform": platform,
            "model": response.model,
            "usage": response.usage
        }


# 全局AI服务实例
ai_service = AIService()

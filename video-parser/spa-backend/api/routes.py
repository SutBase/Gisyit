# -*- coding: utf-8 -*-
"""
API路由
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from .keys import key_manager, APIKey
from .ai_service import ai_service, AIRequest

router = APIRouter()

# API密钥相关路由
@router.post("/keys", response_model=Dict[str, Any])
async def create_api_key(name: str, key: str, description: Optional[str] = None):
    """创建API密钥"""
    try:
        api_key = key_manager.add_key(name, key, description)
        return {
            "success": True,
            "message": "API密钥创建成功",
            "key": {
                "name": api_key.name,
                "description": api_key.description,
                "created_at": api_key.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建API密钥失败: {str(e)}"
        )

@router.get("/keys", response_model=Dict[str, Any])
async def list_api_keys():
    """获取API密钥列表"""
    try:
        keys = key_manager.list_keys()
        return {
            "success": True,
            "keys": list(keys.values())
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取API密钥列表失败: {str(e)}"
        )

@router.put("/keys/{key_name}", response_model=Dict[str, Any])
async def update_api_key(key_name: str, new_key: str, description: Optional[str] = None):
    """更新API密钥"""
    try:
        api_key = key_manager.update_key(key_name, new_key, description)
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API密钥 '{key_name}' 不存在"
            )

        return {
            "success": True,
            "message": "API密钥更新成功",
            "key": {
                "name": api_key.name,
                "description": api_key.description,
                "updated_at": api_key.last_used
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新API密钥失败: {str(e)}"
        )

@router.delete("/keys/{key_name}", response_model=Dict[str, Any])
async def delete_api_key(key_name: str):
    """删除API密钥"""
    try:
        success = key_manager.delete_key(key_name)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"API密钥 '{key_name}' 不存在"
            )

        return {
            "success": True,
            "message": f"API密钥 '{key_name}' 删除成功"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除API密钥失败: {str(e)}"
        )

# AI服务相关路由
@router.post("/ai/generate", response_model=Dict[str, Any])
async def generate_text(request: AIRequest, api_key_name: str = "default"):
    """生成文本"""
    try:
        response = await ai_service.generate_text(request, api_key_name)
        return {
            "success": True,
            "content": response.content,
            "model": response.model,
            "usage": response.usage
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成文本失败: {str(e)}"
        )

@router.post("/ai/analyze-video", response_model=Dict[str, Any])
async def analyze_video(video_data: Dict[str, Any], api_key_name: str = "default"):
    """分析视频内容"""
    try:
        result = await ai_service.analyze_video_content(video_data, api_key_name)
        return {
            "success": True,
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"分析视频内容失败: {str(e)}"
        )

@router.post("/ai/generate-content", response_model=Dict[str, Any])
async def generate_content(
    video_data: Dict[str, Any], 
    content_type: str, 
    platform: Optional[str] = None, 
    api_key_name: str = "default"
):
    """生成内容文案"""
    try:
        result = await ai_service.generate_content_copy(
            video_data, content_type, platform, api_key_name
        )
        return {
            "success": True,
            "result": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"生成内容文案失败: {str(e)}"
        )

@router.post("/ai/correlation-analysis", response_model=Dict[str, Any])
async def correlation_analysis(
    analysis_data: Dict[str, Any], 
    analysis_type: str, 
    api_key_name: str = "default"
):
    """相关性分析"""
    try:
        # 构建分析提示
        if analysis_type == "audience":
            prompt = f"""请对以下内容进行受众分析：

分析目标：{analysis_data.get('target', '')}

请从以下几个方面进行分析：
1. 年龄段分布
2. 性别分布
3. 兴趣标签（5-10个）
4. 活跃时段
5. 内容偏好（按类别和百分比）
6. 针对性策略建议（3-5条）

请以JSON格式返回分析结果。"""

        elif analysis_type == "content":
            prompt = f"""请对以下内容进行内容相关性分析：

分析目标：{analysis_data.get('target', '')}
对比内容：{analysis_data.get('compare', '')}

请从以下几个方面进行分析：
1. 关键词提取和相关性评分
2. 主题分布和权重
3. 与对比内容的多维度相似度分析

请以JSON格式返回分析结果。"""

        elif analysis_type == "trend":
            prompt = f"""请对以下内容进行趋势分析：

分析目标：{analysis_data.get('target', '')}

请从以下几个方面进行分析：
1. 过去30天的热度变化（每日数据）
2. 相关话题和趋势变化
3. 未来1-4周的预测和建议

请以JSON格式返回分析结果。"""

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的分析类型: {analysis_type}"
            )

        # 调用AI生成分析结果
        request = AIRequest(prompt=prompt, model="deepseek-reasoner")
        response = await ai_service.generate_text(request, api_key_name)

        # 尝试解析JSON结果
        try:
            # 查找JSON部分
            content = response.content
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                return {
                    "success": True,
                    "result": json.loads(json_str),
                    "model": response.model,
                    "usage": response.usage
                }
        except:
            pass

        # 如果无法解析JSON，返回原始内容
        return {
            "success": True,
            "result": {
                "analysis": response.content,
                "type": analysis_type
            },
            "model": response.model,
            "usage": response.usage
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"相关性分析失败: {str(e)}"
        )

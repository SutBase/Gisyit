# -*- coding: utf-8 -*-
"""
API密钥管理模块
"""

import os
from typing import Optional, Dict, Any
from pydantic import BaseModel
from fastapi import HTTPException, status
import json
import time

# 密钥存储文件路径
KEYS_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'api_keys.json')

class APIKey(BaseModel):
    """API密钥模型"""
    name: str
    key: str
    description: Optional[str] = None
    created_at: str
    last_used: Optional[str] = None
    usage_count: int = 0

class APIKeyManager:
    """API密钥管理器"""

    def __init__(self):
        self._ensure_data_dir()
        self._keys = self._load_keys()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        data_dir = os.path.dirname(KEYS_FILE_PATH)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _load_keys(self) -> Dict[str, APIKey]:
        """加载API密钥"""
        try:
            if not os.path.exists(KEYS_FILE_PATH):
                return {}

            with open(KEYS_FILE_PATH, 'r', encoding='utf-8') as f:
                keys_data = json.load(f)

            return {
                name: APIKey(**key_data) 
                for name, key_data in keys_data.items()
            }
        except Exception as e:
            print(f"加载API密钥失败: {str(e)}")
            return {}

    def _save_keys(self):
        """保存API密钥"""
        try:
            with open(KEYS_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(
                    {name: key.dict() for name, key in self._keys.items()}, 
                    f, 
                    ensure_ascii=False, 
                    indent=2
                )
        except Exception as e:
            print(f"保存API密钥失败: {str(e)}")

    def add_key(self, name: str, key: str, description: str = None) -> APIKey:
        """添加API密钥"""
        if not name or not key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="密钥名称和密钥不能为空"
            )

        if name in self._keys:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"密钥名称 '{name}' 已存在"
            )

        api_key = APIKey(
            name=name,
            key=key,
            description=description,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )

        self._keys[name] = api_key
        self._save_keys()

        return api_key

    def get_key(self, name: str) -> Optional[APIKey]:
        """获取API密钥"""
        key = self._keys.get(name)
        if key:
            # 更新使用时间和次数
            key.last_used = time.strftime("%Y-%m-%d %H:%M:%S")
            key.usage_count += 1
            self._save_keys()

        return key

    def list_keys(self) -> Dict[str, APIKey]:
        """列出所有API密钥"""
        return {name: APIKey(**key.dict(exclude={'key'})) for name, key in self._keys.items()}

    def delete_key(self, name: str) -> bool:
        """删除API密钥"""
        if name not in self._keys:
            return False

        del self._keys[name]
        self._save_keys()
        return True

    def update_key(self, name: str, new_key: str, description: str = None) -> Optional[APIKey]:
        """更新API密钥"""
        if name not in self._keys:
            return None

        self._keys[name].key = new_key
        if description is not None:
            self._keys[name].description = description

        self._save_keys()
        return self._keys[name]


# 全局API密钥管理器实例
key_manager = APIKeyManager()

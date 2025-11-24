"""
文件作用：
-----------
用于加载测试框架的配置（如base_url、浏览器类型、等待时间等）。
支持从 JSON 文件和环境变量读取配置，以便本地和CI环境都能复用。
"""
import json
import os
from pathlib import Path

import yaml

#项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = BASE_DIR / "config" / "config.json"
# CONFIG_PATH = BASE_DIR / "config" / "config.yaml"

#默认配置
DEFAULTS = {
    "base_url": "http://127.0.0.1:8000",
    "browser": "chrome",
    "headless": False,
    "implicitly_wait": 5,
}

def load_config():
    # 加载config文件
    config = DEFAULTS.copy()
    # 覆盖 config.json 中的配置
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH,"r",encoding="utf-8") as f:
            file_config = json.load(f)
        config.update(file_config)

    return config

def load_data(file_name):
    """加载 data 目录下的 YAML 文件"""
    data_path = BASE_DIR / "data" / file_name
    with open(data_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)
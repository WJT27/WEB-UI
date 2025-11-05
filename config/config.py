"""
文件作用：
-----------
用于加载测试框架的配置（如base_url、浏览器类型、等待时间等）。
支持从 JSON 文件和环境变量读取配置，以便本地和CI环境都能复用。
"""
import json
import os
from pathlib import Path

#项目根目录
BASE_DIR = Path(__file__).resolve().parents[1]

#默认配置
DEFAULTS = {
    "base_url": "http://127.0.0.1:8000",
    "browser": "chrome",
    "headless": False,
    "implicitly_wait": 5,
}

def load_config():
    """加载配置优先级：env > config.json > DEFAULTS"""
    config = DEFAULTS.copy()
    cfg_path = BASE_DIR / "config"/ "config.json"

    # 覆盖 config.json 中的配置
    if cfg_path.exists():
        with open(cfg_path,"r",encoding="utf-8") as f:
            file_config = json.load(f)
        config.update(file_config)

    # 环境变量覆盖
    #config['browser'] = os.getenv("BROWSER",config['browser'])
    #config['headless'] = os.getenv("HEADLESS",config['headless']) in ("True", "true","1")

    return config
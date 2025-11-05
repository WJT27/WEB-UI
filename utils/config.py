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
    "base_url": "http://132.122.1.215:6300",
    "browser": "chrome",
    "headless": False,
    "implicitly_wait": 5,
}

def load_config():
    """
    加载配置逻辑：
    1. 先从项目根目录查找 config.json；
    2. 如果存在，则覆盖默认配置；
    3. 支持通过环境变量（BROWSER、HEADLESS）进一步覆盖。
    """
    cfg_path = BASE_DIR / "config.json"
    if cfg_path.exists():
        with open(cfg_path) as f:
            cfg = json.load(f)
        DEFAULTS.update(cfg)
    DEFAULTS['browser'] = os.getenv("BROWSER",DEFAULTS['browser'])
    DEFAULTS['headless'] = os.getenv("HEADLESS",DEFAULTS['headless']) in ("True", "true","1")
    return DEFAULTS
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """全局配置，支持从环境变量或 .env 读取。"""

    app_name: str = "Study Agent"
    debug: bool = True

    # 数据库配置（默认使用本地 SQLite，便于本地开发）
    database_url: str = "sqlite+aiosqlite:///./study_agent.db"

    # Redis（会话记忆）
    redis_url: str = "redis://localhost:6379/0"

    # LLM / 阿里云百炼 DashScope API
    dashscope_api_key: str | None = None  # 阿里云百炼 API Key
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 默认北京地域，可改为 dashscope-intl.aliyuncs.com（新加坡）或 dashscope-us.aliyuncs.com（美国）

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """获取全局单例配置。"""
    return Settings()


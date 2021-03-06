from typing import List
from functools import lru_cache

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Standard"

    LOG_LEVEL: str = "DEBUG"  # TRACE, INFO, SUCCESS, WARNING, ERROR, CRITICAL ...

    API_V1_STR: str = "/api/v1"
    API_LOGIN_URL: str = "/api/v1/login"

    SECRET_KEY: str = "-tWkxu3b0nkzgxU6KwkpTr9WDWpz-cBNKlvwvRnzTng"
    SALT_ROUNDS: int = 4

    # JWT expiration time
    ACCESS_TOKEN_EXPIRES_MINUTES: int = 60 * 24

    # timezone
    TIMEZONE: str = "Asia/Shanghai"

    # Cross-domain request configuration
    BACKEND_CORS_ORIGINS: List = ["*"]

    # Database configuration
    # Use by default sqlite3
    # user sqlite3 config 
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./myproject.sqlite3"

    # user mysql config
    # DATABASE_USER: str = "root"
    # DATABASE_PASS: str = "root"
    # DATABASE_HOST: str = "192.168.1.8"
    # DATABASE_DB: str = "Standard"
    # DATABASE_PORT: str = "3308"
    # SQLALCHEMY_DATABASE_URI: str = f"mysql+pymysql://" \
    #                                f"{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"


    # Redis store address
    REDIS_STORAGE_HOST: str = "localhost"
    REDIS_STORAGE_PORT: str = "6379"
    REDIS_STORAGE_PASS: str = ""

    # RateLimitBackend
    RATE_LIMIT_REDIS_BACKEND_HOST: str = "localhost"
    RATE_LIMIT_REDIS_BACKEND_PORT: str = "6379"
    RATE_LIMIT_REDIS_BACKEND_DB: str = "0"
    RATE_LIMIT_REDIS_BACKEND_PASS: str = ""

    # Celery broker & backend
    CELERY_BROKER: str = ""
    CELERY_BACKEND: str = ""

    # Add needed to encrypt communication url
    EXURL=['/api/v1/rbac/dataset1/protected']
    class Config:
        case_sensitive = True


@lru_cache(1)
def get_config():
    devops_server_host = 'http://'
    api_key = ''
    app = ''
    from dotenv import load_dotenv, find_dotenv
    if find_dotenv():
        logger.debug('Locate .env file and configure the project with.env')
        load_dotenv(encoding='utf8')
        return Settings()
    else:
        import json
        import os
        import requests

        dev_mode = os.getenv('DEV_MODE', 'dev')
        assert dev_mode in ['test', 'stable', 'dev']
        if dev_mode == 'stable':
            logger.debug('??????????????????, ??????????????????????????????')
        elif dev_mode == 'test':
            logger.debug('??????????????????, ??????????????????????????????')
        else:
            logger.debug('?????????????????????')

        if dev_mode != 'dev':
            devops_api = f'{devops_server_host}/api/apis/config/?apiKey={api_key}&app={app}&env={dev_mode}' \
                         f'&format=json&noPrefix=1'
            r = requests.get(devops_api)
            if r.status_code != 200:
                raise RuntimeError('???????????????????????????')
            env = json.loads(r.text)

            for key, value in env.items():
                os.environ[key] = value
        logger.debug('????????????????????????')
        return Settings()


settings = get_config()

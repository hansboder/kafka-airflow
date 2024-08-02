from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    github_url: str
    github_pat: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

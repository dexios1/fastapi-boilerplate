"""
The :mod:`app.core.config` module contains dataclasses 
containing settings information for the api application.
"""
# Author: Chris Dare
# License:
import logging
import os
import secrets
from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = os.environ["SERVER_NAME"]
    SERVER_HOST: AnyHttpUrl = os.environ["SERVER_HOST"]
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000",]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.environ["BACKEND_CORS_ORIGINS"]
    NEO4J_DATABASE_URI: str = f"bolt://{os.environ['NEO4J_USER']}:{os.environ['NEO4J_PASSWORD']}@{os.environ['NEO4J_HOST']}"
    

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    class Config:
        case_sensitive = True


settings = Settings()

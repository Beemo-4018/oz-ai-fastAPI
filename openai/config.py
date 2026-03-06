# 환경 구성(configuration) 관리 파일
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    open_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        # utf-8-sig로 설정하면 파일 맨 앞의 BOM(\ufeff)을 자동으로 제거하고 읽습니다.
        env_file_encoding="utf-8-sig",
    )


settings = Settings()

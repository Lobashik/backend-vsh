from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

	app_name: str = "Images API"
	api_prefix: str = "/api"
	jwt_secret_key: str = "change-me"
	jwt_algorithm: str = "HS256"
	access_token_expire_minutes: int = 120
	storage_dir: str = "./data/files"
	cors_origins: list[str] = Field(default_factory=lambda: ["*"])

	@field_validator("cors_origins", mode="before")
	@classmethod
	def parse_cors_origins(cls, value: object) -> list[str]:
		if isinstance(value, str):
			return [item.strip() for item in value.split(",") if item.strip()]
		if isinstance(value, list):
			return [str(item).strip() for item in value if str(item).strip()]
		return ["*"]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
	return Settings()

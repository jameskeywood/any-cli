from __future__ import annotations

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    gemini_api_key: str | None = None
    groq_api_key: str |None = None
    openrouter_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    @property
    def provider_api_keys(self) -> dict[str, str]:
        """
        Return configured providers and their API keys.

        Providers without keys are excluded.
        """

        providers = {
            "gemini": self.gemini_api_key,
            "groq": self.groq_api_key,
            "openrouter": self.openrouter_api_key,
        }

        return {
            provider: api_key
            for provider, api_key in providers.items()
            if api_key
        }


settings = Settings()

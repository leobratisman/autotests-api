from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_BASE_URL: str
    API_AUTH_URL: str
    TIMEOUT: int

    TEST_DATA_DIR: str

    def file_path(self, filename: str) -> str:
        return str(self.TEST_DATA_DIR) + filename

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()

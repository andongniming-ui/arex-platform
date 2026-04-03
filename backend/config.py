from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_type: str = "sqlite"
    db_url: str = "sqlite+aiosqlite:////app/data/arex_platform.db"
    secret_key: str = "changeme"
    ssh_keys_dir: str = "/app/ssh_keys"
    cors_origins: str = "*"
    # AREX-specific settings
    arex_storage_url: str = "http://arex-storage:8080"
    arex_agent_jar_path: str = "/opt/arex-agent/arex-agent.jar"

    class Config:
        env_prefix = "AP_"

settings = Settings()

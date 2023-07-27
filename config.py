from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    motion_api_key: str
    workspace_name: str
    linear_api_key: str
    linear_email: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

# Load and validate the configuration
config = AppConfig()

motion_api_key = config.motion_api_key
workspace_name = config.workspace_name
linear_api_key = config.linear_api_key
linear_email = config.linear_email

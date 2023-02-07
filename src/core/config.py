from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class AppSettings(BaseSettings):
    project_name: str = 'FileManager'
    project_host: str = '127.0.0.1'
    project_port: int = 8080
    reset_password: str = 'SECRET_1'
    verification: str = 'SECRET_2'
    files_dir: str = 'static_files'
    blacklisted_ips: list[str, None] = []
    database_dsn: PostgresDsn = ...

    class Config:
        env_file = '.env'


app_settings = AppSettings()

import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()


class AppSettings(BaseSettings):
    title: str = os.environ.get('PROJECT_NAME', 'FileManager')
    host: str = os.environ.get('PROJECT_HOST', '127.0.0.1')
    port: int = int(os.environ.get('PROJECT_PORT', 8080))
    reset_password: str = os.environ.get('RESET_PASSWORD', 'SECRET_1')
    verification: str = os.environ.get('VERIFICATION', 'SECRET_2')
    file_path: str = os.environ.get('FILES_DIR', 'static_files')
    blacklisted_ips: list[str, None] = os.environ.get('BLACKLISTED_IPS', [])
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings()

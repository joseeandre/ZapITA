from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "fast_api_app"
    bucket: str = "ces22-datalake-develop"
    prefix: str = "python-template/fast-api"
    temp_folder: str = "/home/vscode/temp"
    s3_output_path: str = "s3://athena-logs-develop/"
    datalake_db: str = "db_template_scala"

    class Config:
        env_file = "app/.env"

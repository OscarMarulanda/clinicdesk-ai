from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://localhost:5432/clinicdesk"

    # Anthropic
    anthropic_api_key: str = ""

    # SendGrid
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "oscarmarulandab@gmail.com"

    # Google Calendar
    google_credentials_path: str = "./credentials.json"
    google_calendar_id: str = "primary"

    # App
    app_secret_key: str = "change-me-in-production"
    app_env: str = "development"
    app_port: int = 8000
    support_team_email: str = "oscarmarulandab@gmail.com"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()

from pydantic import BaseSettings, Field, HttpUrl


class WorkflowSettings(BaseSettings):
    API_ENDPOINT: HttpUrl = Field(
        default="http://127.0.0.1:6663",
        description="URL for elice API server.",
    )

    RESPONSE_VERIFY_DICT: dict[str, str] = Field(
        default={},
        description="Response validation for elice API server.",
    )

    class Config:
        env_file = ".env.esbt"
        env_prefix = "esbt_"

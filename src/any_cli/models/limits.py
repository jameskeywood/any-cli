from pydantic import BaseModel


class ModelLimits(BaseModel):
    requests_per_minute: int | None = None
    requests_per_day: int | None = None

    tokens_per_minute: int | None = None
    tokens_per_day: int | None = None

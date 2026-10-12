from pydantic import BaseModel, Field, field_validator


class NormalizedListing(BaseModel):
    external_id: str = Field(min_length=1, max_length=160)
    title: str = Field(min_length=1, max_length=255)
    description: str = ""
    price_vnd: int | None = Field(default=None, ge=0)
    area_m2: float = Field(gt=0)
    province_code: str = ""
    commune_code: str = ""
    source: str
    contact_phone: str = ""

    @field_validator("source")
    @classmethod
    def source_required(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("source is required")
        return value.strip()

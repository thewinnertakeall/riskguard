from pydantic import BaseModel, ConfigDict, Field


class DatasetCreateDTO(BaseModel):
    code: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=255)
    description: str = ""
    source_type: str = Field(min_length=1, max_length=30)
    source_location: str = Field(min_length=1, max_length=1000)
    record_count: int = Field(default=0, ge=0)
    active: bool = True


class DatasetUpdateDTO(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    source_type: str | None = Field(default=None, max_length=30)
    source_location: str | None = Field(default=None, max_length=1000)
    record_count: int | None = Field(default=None, ge=0)
    active: bool | None = None


class DatasetResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    description: str
    source_type: str
    source_location: str
    record_count: int
    active: bool
    created_at: str | None = None
    updated_at: str | None = None

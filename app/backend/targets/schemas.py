from pydantic import BaseModel, Field
from datetime import datetime


class RawTarget(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=300)
    status: str = Field(default='new')


class DetailedTarget(RawTarget):
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdatedTarget(DetailedTarget):
    updated_at: datetime


class DeletedTarget(UpdatedTarget):
    deleted_at: datetime

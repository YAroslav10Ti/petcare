from datetime import date, datetime

from pydantic import BaseModel, ConfigDict



class PetCreate(BaseModel):
    name: str
    species: str
    breed: str | None = None
    birth_date: date | None = None
    sex: str | None = None
    age: int | None = None
    weight_kg: float | None = None
    notes: str | None = None


class PetUpdate(BaseModel):
    name: str | None = None
    species: str | None = None
    breed: str | None = None
    birth_date: date | None = None
    sex: str | None = None
    age: int | None = None
    weight_kg: float | None = None
    notes: str | None = None


class PetResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    species: str
    breed: str | None
    birth_date: date | None
    sex: str | None
    weight_kg: float | None
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
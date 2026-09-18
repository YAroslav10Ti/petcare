from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class MedicalRecordCreate(BaseModel):
    pet_id: int
    visit_date: date
    title: str 
    diagnosis: str | None = None
    symptoms: str | None = None
    treatment: str | None = None
    notes: str | None = None
    created_at: datetime  


class MedicalRecordResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pet_id: int
    visit_date: date
    title: str 
    diagnosis: str | None = None
    symptoms: str | None = None
    treatment: str | None = None
    notes: str | None = None
    created_at: datetime

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.medical_record import MedicalRecord
from app.api.v1.medical_record.schemas import MedicalRecordCreate, MedicalRecordResponse
from app.models.pet import Pet
from app.models.user import User

medical_router = APIRouter(
    prefix="/medical-records",
    tags=["Medical Records"],
)


@medical_router.post("", response_model=MedicalRecordResponse, status_code=status.HTTP_201_CREATED)
def create_medical_record(data: MedicalRecordCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check if the pet belongs to the current user
    pet = db.query(Pet).filter(Pet.id == data.pet_id, Pet.owner_id == current_user.id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")

    medical_record = MedicalRecord(
        pet_id=data.pet_id,
        visit_date=data.visit_date,
        title=data.title,
        diagnosis=data.diagnosis,
        symptoms=data.symptoms,
        treatment=data.treatment,
        notes=data.notes,
        created_at=data.created_at
    )

    db.add(medical_record)
    db.commit()
    db.refresh(medical_record)
    return medical_record



@medical_router.get("", response_model = list[MedicalRecordResponse], status_code=status.HTTP_200_OK)
def get_medical_records(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    medical_records = db.query(MedicalRecord).join(Pet).filter(Pet.owner_id == current_user.id).all()
    return medical_records
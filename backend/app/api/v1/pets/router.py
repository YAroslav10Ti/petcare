from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.auth.dependencies import get_current_user
from app.api.v1.pets.schemas import PetCreate, PetResponse
from app.core.database import get_db
from app.models.pet import Pet
from app.models.user import User





pets_router = APIRouter(
    prefix = "/pets",
    tags = ["Pets"],
)

@pets_router.get("", response_model = list[PetResponse], status_code = status.HTTP_200_OK)
def get_pets(current_user: User = Depends(get_current_user), db: Session =Depends(get_db)):
    pets = db.query(Pet).filter(Pet.owner_id == current_user.id).all()
    return pets


@pets_router.post("", response_model = PetResponse, status_code = status.HTTP_201_CREATED)
def create_pet(data: PetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = Pet(
        owner_id = current_user.id,
        name = data.name,
        species = data.species,
        breed = data.breed,
        birth_date = data.birth_date,
        sex = data.sex,
        weight_kg = data.weight_kg,
        notes = data.notes,
    )

    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@pets_router.delete("/{pet_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_pet(pet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == current_user.id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    
    db.delete(pet)
    db.commit()


@pets_router.put("/{pet_id}", response_model = PetResponse, status_code = status.HTTP_200_OK)
def update_pet(pet_id: int, data: PetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db), status_code = status.HTTP_200_OK):
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == current_user.id).first()
    if not pet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found")
    pet.name = data.name
    pet.species = data.species
    pet.breed = data.breed
    pet.birth_date = data.birth_date
    pet.sex = data.sex
    pet.weight_kg = data.weight_kg
    pet.notes = data.notes

    db.commit()
    db.refresh(pet)
    return pet
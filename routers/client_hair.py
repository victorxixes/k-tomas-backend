from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ClientHairProfile
from schemas import HairProfileCreate, HairProfileResponse

router = APIRouter(prefix="/hair", tags=["Hair Profile"])

@router.post("/", response_model=HairProfileResponse)
def create_hair_profile(data: HairProfileCreate, db: Session = Depends(get_db)):
    profile = ClientHairProfile(**data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

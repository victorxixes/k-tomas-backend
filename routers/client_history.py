from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ClientHistory
from schemas import HistoryCreate, HistoryResponse

router = APIRouter(prefix="/history", tags=["Client History"])

@router.post("/", response_model=HistoryResponse)
def create_history_entry(data: HistoryCreate, db: Session = Depends(get_db)):
    entry = ClientHistory(**data.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

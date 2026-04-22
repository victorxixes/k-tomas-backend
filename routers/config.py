from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Horarios, ServiceConfig
import json

router = APIRouter(prefix="/config", tags=["Config"])


# --------------------------
# HORARIOS
# --------------------------
@router.get("/horarios")
def get_horarios(db: Session = Depends(get_db)):
    h = db.query(Horarios).first()
    if not h:
        return {
            "apertura": "09:00",
            "cierre": "20:00",
            "dias_laborables": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
        }

    return {
        "apertura": h.apertura,
        "cierre": h.cierre,
        "dias_laborables": json.loads(h.dias_laborables),
    }


@router.put("/horarios")
def update_horarios(data: dict, db: Session = Depends(get_db)):
    h = db.query(Horarios).first()

    if not h:
        h = Horarios()

    h.apertura = data["apertura"]
    h.cierre = data["cierre"]
    h.dias_laborables = json.dumps(data["dias_laborables"])

    db.add(h)
    db.commit()

    return {"status": "ok"}


# --------------------------
# SERVICIOS
# --------------------------
@router.get("/servicios")
def get_servicios(db: Session = Depends(get_db)):
    return db.query(ServiceConfig).all()

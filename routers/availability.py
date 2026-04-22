from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
import backend.models as models
from backend.utils.availability import calculate_free_slots_backend
from backend.config.stylists import STYLISTS

router = APIRouter(prefix="/availability", tags=["availability"])


@router.get("/")
def get_availability(date: str, service: str, stylist: str, db: Session = Depends(get_db)):
    # Validación básica
    if stylist not in STYLISTS:
        raise HTTPException(status_code=400, detail="Estilista no válido")

    if service not in STYLISTS[stylist]["services"]:
        raise HTTPException(status_code=400, detail="Servicio no válido para este estilista")

    # Obtener citas del día
    appointments = (
        db.query(models.Appointment)
        .filter(models.Appointment.date == date)
        .filter(models.Appointment.stylist == stylist)
        .all()
    )

    # Calcular huecos libres
    free_slots = calculate_free_slots_backend(date, service, stylist, appointments)

    return {
        "date": date,
        "service": service,
        "stylist": stylist,
        "free_slots": free_slots
    }

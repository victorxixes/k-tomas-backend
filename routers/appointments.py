from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
import backend.models as models
import backend.schemas as schemas

from backend.utils.availability import get_duration, add_minutes
from backend.config.stylists import STYLISTS

router = APIRouter(prefix="/appointments", tags=["appointments"])


# ---------------------------------------------------------
# GET: listar citas (opcionalmente por fecha)
# ---------------------------------------------------------
@router.get("/", response_model=list[schemas.Appointment])
def list_appointments(date: str | None = None, db: Session = Depends(get_db)):
    query = db.query(models.Appointment)
    if date:
        query = query.filter(models.Appointment.date == date)
    return query.all()

# ---------------------------------------------------------
# POST: crear cita con validación de solapamientos
# ---------------------------------------------------------
@router.post("/", response_model=schemas.Appointment)
def create_appointment(data: schemas.AppointmentCreate, db: Session = Depends(get_db)):

    # Validación: estilista existe
    if data.stylist not in STYLISTS:
        raise HTTPException(status_code=400, detail="Estilista no válido")

    # Obtener citas del mismo estilista en ese día
    existing = (
        db.query(models.Appointment)
        .filter(models.Appointment.date == data.date)
        .filter(models.Appointment.stylist == data.stylist)
        .all()
    )

    # Calcular duración real
    duration = get_duration(data.service, data.stylist)
    new_start = data.time.strftime("%H:%M")
    new_end = add_minutes(new_start, duration)

    # Validación de solapamientos
    for cita in existing:
        cita_start = cita.time.strftime("%H:%M")
        cita_end = add_minutes(cita_start, get_duration(cita.service, cita.stylist))

        if not (new_end <= cita_start or new_start >= cita_end):
            raise HTTPException(status_code=400, detail="Cita solapada")

    # Guardar cita
    appt = models.Appointment(**data.model_dump())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

# ---------------------------------------------------------
# DELETE: eliminar cita
# ---------------------------------------------------------
@router.delete("/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    db.delete(appt)
    db.commit()
    return {"status": "deleted"}

# ---------------------------------------------------------
# PUT: actualizar cita
# ---------------------------------------------------------
@router.put("/{id}", response_model=schemas.Appointment)
def update_appointment(id: int, data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Actualizar campos
    for key, value in data.model_dump().items():
        setattr(appt, key, value)

    db.commit()
    db.refresh(appt)
    return appt

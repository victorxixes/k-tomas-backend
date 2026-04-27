from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.client import Client
from app.models.service_history import ServiceHistory
from app.schemas.service_history import ServiceHistoryCreate, ServiceHistoryOut

router = APIRouter(prefix="/services-history", tags=["services-history"])


@router.post("/", response_model=ServiceHistoryOut)
def add_service(entry: ServiceHistoryCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == entry.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db_entry = ServiceHistory(**entry.model_dump())
    db.add(db_entry)

    # actualizar métricas del cliente
    client.total_servicios += 1
    client.total_facturado += entry.price
    client.ultimo_servicio_importe = entry.price
    client.ultimo_servicio_fecha = db_entry.date

    if not entry.paid:
        client.impagos_total += 1
        client.impagos_importe += entry.price

    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/client/{client_id}", response_model=List[ServiceHistoryOut])
def list_client_services(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    entries = (
        db.query(ServiceHistory)
        .filter(ServiceHistory.client_id == client_id)
        .order_by(ServiceHistory.date.desc())
        .all()
    )
    return entries

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, date

import models
import schemas
from database import SessionLocal

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI()

# CORS (solo una vez y después de crear app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego puedes poner tu dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# DB SESSION
# ============================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# APPOINTMENTS
# ============================================================

@app.get("/appointments", response_model=list[schemas.Appointment])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()


@app.post("/appointments", response_model=schemas.Appointment)
def create_appointment(appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    new = models.Appointment(**appt.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.put("/appointments/{id}", response_model=schemas.Appointment)
def update_appointment(id: int, data: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    for key, value in data.dict().items():
        setattr(appt, key, value)
    db.commit()
    db.refresh(appt)
    return appt


@app.delete("/appointments/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    db.delete(appt)
    db.commit()
    return {"ok": True}

# ============================================================
# CLIENTS
# ============================================================

@app.get("/clients", response_model=list[schemas.Client])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()


@app.get("/clients/{client_id}", response_model=schemas.Client)
def get_client(client_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return c


@app.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    new = models.Client(
        **client.dict(),
        created_at=datetime.now().isoformat()
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.put("/clients/{id}", response_model=schemas.Client)
def update_client(id: int, data: schemas.ClientCreate, db: Session = Depends(get_db)):
    c = db.query(models.Client).filter(models.Client.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for key, value in data.dict().items():
        setattr(c, key, value)
    db.commit()
    db.refresh(c)
    return c


@app.delete("/clients/{id}")
def delete_client(id: int, db: Session = Depends(get_db)):
    c = db.query(models.Client).filter(models.Client.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(c)
    db.commit()
    return {"ok": True}

# ============================================================
# (TODO: resto de endpoints — NO LOS REPITO AQUÍ)
# ============================================================

# Puedes dejar todos los demás endpoints tal cual estaban.
# El único problema real era el orden de creación de `app`
# y la duplicación del middleware CORS.

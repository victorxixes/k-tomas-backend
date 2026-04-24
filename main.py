from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from datetime import date, datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# DB SESSION
# -------------------------
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
# CLIENTS (FICHA COMPLETA)
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
# CLIENT FISCAL DATA
# ============================================================
@app.get("/clients/{client_id}/fiscal", response_model=schemas.ClientFiscalData)
def get_client_fiscal(client_id: int, db: Session = Depends(get_db)):
    data = db.query(models.ClientFiscalData).filter(models.ClientFiscalData.client_id == client_id).first()
    if not data:
        raise HTTPException(status_code=404, detail="Datos fiscales no encontrados")
    return data


@app.post("/clients/{client_id}/fiscal", response_model=schemas.ClientFiscalData)
def create_or_update_client_fiscal(client_id: int, payload: schemas.ClientFiscalDataCreate, db: Session = Depends(get_db)):
    data = db.query(models.ClientFiscalData).filter(models.ClientFiscalData.client_id == client_id).first()
    if not data:
        data = models.ClientFiscalData(client_id=client_id, **payload.dict())
        db.add(data)
    else:
        for k, v in payload.dict().items():
            setattr(data, k, v)
    db.commit()
    db.refresh(data)
    return data


# ============================================================
# CLIENT TECHNICAL SHEET
# ============================================================
@app.get("/clients/{client_id}/technical", response_model=schemas.ClientTechnicalSheet)
def get_client_technical(client_id: int, db: Session = Depends(get_db)):
    sheet = db.query(models.ClientTechnicalSheet).filter(models.ClientTechnicalSheet.client_id == client_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Ficha técnica no encontrada")
    return sheet


@app.post("/clients/{client_id}/technical", response_model=schemas.ClientTechnicalSheet)
def create_or_update_client_technical(client_id: int, payload: schemas.ClientTechnicalSheetCreate, db: Session = Depends(get_db)):
    sheet = db.query(models.ClientTechnicalSheet).filter(models.ClientTechnicalSheet.client_id == client_id).first()
    if not sheet:
        sheet = models.ClientTechnicalSheet(client_id=client_id, **payload.dict())
        db.add(sheet)
    else:
        for k, v in payload.dict().items():
            setattr(sheet, k, v)
    db.commit()
    db.refresh(sheet)
    return sheet


# ============================================================
# CLIENT CONSENT
# ============================================================
@app.get("/clients/{client_id}/consent", response_model=schemas.ClientConsent)
def get_client_consent(client_id: int, db: Session = Depends(get_db)):
    consent = db.query(models.ClientConsent).filter(models.ClientConsent.client_id == client_id).first()
    if not consent:
        raise HTTPException(status_code=404, detail="Consentimientos no encontrados")
    return consent


@app.post("/clients/{client_id}/consent", response_model=schemas.ClientConsent)
def create_or_update_client_consent(client_id: int, payload: schemas.ClientConsentCreate, db: Session = Depends(get_db)):
    consent = db.query(models.ClientConsent).filter(models.ClientConsent.client_id == client_id).first()
    if not consent:
        consent = models.ClientConsent(client_id=client_id, **payload.dict())
        db.add(consent)
    else:
        for k, v in payload.dict().items():
            setattr(consent, k, v)
    db.commit()
    db.refresh(consent)
    return consent


# ============================================================
# LOPD: SUBIDA DOCUMENTO + ENVÍO EMAIL (SIMULADO)
# ============================================================
@app.post("/clients/{client_id}/lopd/upload", response_model=schemas.ClientConsent)
def upload_lopd_document(client_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    consent = db.query(models.ClientConsent).filter(models.ClientConsent.client_id == client_id).first()
    if not consent:
        consent = models.ClientConsent(client_id=client_id)
        db.add(consent)
        db.commit()
        db.refresh(consent)

    # Aquí deberías guardar el fichero en disco o en un storage externo
    consent.lopd_document_url = f"/static/lopd/{client_id}/{file.filename}"
    consent.lopd_signed = True

    db.commit()
    db.refresh(consent)
    return consent


@app.post("/clients/{client_id}/lopd/send-email")
def send_lopd_email(client_id: int):
    # Aquí iría la lógica real de envío de email
    return {"ok": True, "message": "LOPD enviada por email (simulado)"}


# ============================================================
# CLIENT HAIR PROFILE
# ============================================================
@app.post("/clients/{client_id}/hair", response_model=schemas.HairProfile)
def create_hair_profile(client_id: int, data: schemas.HairProfileCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    profile = models.ClientHairProfile(
        client_id=client_id,
        **data.dict()
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@app.get("/clients/{client_id}/hair", response_model=list[schemas.HairProfile])
def get_hair_profiles(client_id: int, db: Session = Depends(get_db)):
    return db.query(models.ClientHairProfile).filter(
        models.ClientHairProfile.client_id == client_id
    ).all()


# ============================================================
# CLIENT HISTORY
# ============================================================
@app.post("/clients/{client_id}/history", response_model=schemas.History)
def create_history_entry(client_id: int, data: schemas.HistoryCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    entry = models.ClientHistory(
        client_id=client_id,
        **data.dict()
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@app.get("/clients/{client_id}/history", response_model=list[schemas.History])
def get_client_history(client_id: int, db: Session = Depends(get_db)):
    return db.query(models.ClientHistory).filter(
        models.ClientHistory.client_id == client_id
    ).all()


# ============================================================
# SERVICES
# ============================================================
@app.get("/services", response_model=list[schemas.Service])
def get_services(db: Session = Depends(get_db)):
    return db.query(models.ServiceConfig).all()


@app.post("/services", response_model=schemas.Service)
def create_service(s: schemas.ServiceCreate, db: Session = Depends(get_db)):
    new = models.ServiceConfig(**s.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.put("/services/{id}", response_model=schemas.Service)
def update_service(id: int, data: schemas.ServiceCreate, db: Session = Depends(get_db)):
    s = db.query(models.ServiceConfig).filter(models.ServiceConfig.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    for k, v in data.dict().items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return s


@app.delete("/services/{id}")
def delete_service(id: int, db: Session = Depends(get_db)):
    s = db.query(models.ServiceConfig).filter(models.ServiceConfig.id == id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    db.delete(s)
    db.commit()
    return {"ok": True}


# ============================================================
# PRODUCTS
# ============================================================
@app.get("/products", response_model=list[schemas.Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@app.post("/products", response_model=schemas.Product)
def create_product(p: schemas.ProductCreate, db: Session = Depends(get_db)):
    new = models.Product(**p.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.put("/products/{id}", response_model=schemas.Product)
def update_product(id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    p = db.query(models.Product).filter(models.Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Product).filter(models.Product.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}


# ============================================================
# SCHEDULE
# ============================================================
@app.get("/schedule", response_model=list[schemas.Schedule])
def get_schedule(db: Session = Depends(get_db)):
    return db.query(models.Horarios).all()


@app.post("/schedule", response_model=schemas.Schedule)
def create_schedule(h: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    new = models.Horarios(**h.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@app.put("/schedule/{id}", response_model=schemas.Schedule)
def update_schedule(id: int, data: schemas.ScheduleCreate, db: Session = Depends(get_db)):
    h = db.query(models.Horarios).filter(models.Horarios.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    for k, v in data.dict().items():
        setattr(h, k, v)
    db.commit()
    db.refresh(h)
    return h


@app.delete("/schedule/{id}")
def delete_schedule(id: int, db: Session = Depends(get_db)):
    h = db.query(models.Horarios).filter(models.Horarios.id == id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    db.delete(h)
    db.commit()
    return {"ok": True}


# ============================================================
# DASHBOARD
# ============================================================
@app.get("/stats/overview")
def stats_overview(db: Session = Depends(get_db)):
    today_str = date.today().isoformat()

    total_clients = db.query(models.Client).count()
    total_appointments_today = db.query(models.Appointment).filter(
        models.Appointment.date == today_str
    ).count()

    return {
        "total_clients": total_clients,
        "appointments_today": total_appointments_today,
        "revenue": 0,
    }

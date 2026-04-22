from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
from datetime import date

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# APPOINTMENTS
# -------------------------
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
    for key, value in data.dict().items():
        setattr(appt, key, value)
    db.commit()
    db.refresh(appt)
    return appt

@app.delete("/appointments/{id}")
def delete_appointment(id: int, db: Session = Depends(get_db)):
    appt = db.query(models.Appointment).filter(models.Appointment.id == id).first()
    db.delete(appt)
    db.commit()
    return {"ok": True}


# -------------------------
# CLIENTS
# -------------------------
@app.get("/clients", response_model=list[schemas.Client])
def get_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.post("/clients", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    new = models.Client(**client.dict())
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@app.put("/clients/{id}", response_model=schemas.Client)
def update_client(id: int, data: schemas.ClientCreate, db: Session = Depends(get_db)):
    c = db.query(models.Client).filter(models.Client.id == id).first()
    for key, value in data.dict().items():
        setattr(c, key, value)
    db.commit()
    db.refresh(c)
    return c

@app.delete("/clients/{id}")
def delete_client(id: int, db: Session = Depends(get_db)):
    c = db.query(models.Client).filter(models.Client.id == id).first()
    db.delete(c)
    db.commit()
    return {"ok": True}


# -------------------------
# SERVICES
# -------------------------
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
    for k, v in data.dict().items():
        setattr(s, k, v)
    db.commit()
    db.refresh(s)
    return s

@app.delete("/services/{id}")
def delete_service(id: int, db: Session = Depends(get_db)):
    s = db.query(models.ServiceConfig).filter(models.ServiceConfig.id == id).first()
    db.delete(s)
    db.commit()
    return {"ok": True}


# -------------------------
# PRODUCTS
# -------------------------
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
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    p = db.query(models.Product).filter(models.Product.id == id).first()
    db.delete(p)
    db.commit()
    return {"ok": True}


# -------------------------
# SCHEDULE
# -------------------------
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
    for k, v in data.dict().items():
        setattr(h, k, v)
    db.commit()
    db.refresh(h)
    return h

@app.delete("/schedule/{id}")
def delete_schedule(id: int, db: Session = Depends(get_db)):
    h = db.query(models.Horarios).filter(models.Horarios.id == id).first()
    db.delete(h)
    db.commit()
    return {"ok": True}


# -------------------------
# DASHBOARD
# -------------------------
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

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, Client
from sqlalchemy import func
from datetime import date, datetime, timedelta

router = APIRouter(prefix="/stats", tags=["Stats avanzadas"])


# ---------------------------------------------------------
# 1. CITAS DEL DÍA
# ---------------------------------------------------------
@router.get("/citas/hoy")
def citas_hoy(db: Session = Depends(get_db)):
    today = date.today()

    rows = (
        db.query(
            Appointment.id,
            Appointment.time,
            Appointment.service,
            Client.name.label("client"),
        )
        .join(Client, Client.id == Appointment.client_id)
        .filter(Appointment.date == today)
        .order_by(Appointment.time)
        .all()
    )

    return [
        {
            "id": r.id,
            "time": r.time.strftime("%H:%M"),
            "client": r.client,
            "service": r.service,
        }
        for r in rows
    ]


# ---------------------------------------------------------
# 2. INGRESOS POR SERVICIO (MES ACTUAL)
# ---------------------------------------------------------
@router.get("/ingresos/servicio")
def ingresos_por_servicio(db: Session = Depends(get_db)):
    today = date.today()
    month_start = today.replace(day=1)

    rows = (
        db.query(Appointment.service, func.sum(Appointment.price))
        .filter(Appointment.date >= month_start)
        .group_by(Appointment.service)
        .order_by(func.sum(Appointment.price).desc())
        .all()
    )

    return [{"service": r[0], "total": r[1]} for r in rows]


# ---------------------------------------------------------
# 3. CLIENTES NUEVOS POR MES (ÚLTIMOS 12 MESES)
# ---------------------------------------------------------
@router.get("/clientes/nuevos-mes")
def clientes_nuevos_mes(db: Session = Depends(get_db)):
    today = date.today()
    data = []

    for i in range(12):
        month_date = today.replace(day=1) - timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)

        count = (
            db.query(Client)
            .filter(Client.created_at >= month_start)
            .filter(Client.created_at < next_month)
            .count()
        )

        data.append(
            {
                "month": month_start.strftime("%b %Y"),
                "count": count,
            }
        )

    return list(reversed(data))


# ---------------------------------------------------------
# 4. OCUPACIÓN SEMANAL (ÚLTIMOS 7 DÍAS)
# ---------------------------------------------------------
@router.get("/ocupacion/semanal")
def ocupacion_semanal(db: Session = Depends(get_db)):
    today = date.today()
    data = []

    for i in range(7):
        day = today - timedelta(days=i)
        count = db.query(Appointment).filter(Appointment.date == day).count()

        data.append(
            {
                "day": day.strftime("%A"),
                "count": count,
            }
        )

    return list(reversed(data))


# ---------------------------------------------------------
# 5. ALERTAS
# ---------------------------------------------------------
@router.get("/alertas")
def alertas(db: Session = Depends(get_db)):
    now = datetime.now()
    today = date.today()

    # Citas próximas (3 horas)
    three_hours = (now + timedelta(hours=3)).time()

    proximas = (
        db.query(
            Appointment.time,
            Client.name.label("client"),
        )
        .join(Client)
        .filter(Appointment.date == today)
        .filter(Appointment.time >= now.time())
        .filter(Appointment.time <= three_hours)
        .order_by(Appointment.time)
        .all()
    )

    proximas_list = [
        {
            "client": r.client,
            "time": r.time.strftime("%H:%M"),
        }
        for r in proximas
    ]

    # Clientes sin volver (60 días)
    sixty_days_ago = today - timedelta(days=60)

    rows = (
        db.query(Client.name, func.max(Appointment.date))
        .join(Appointment)
        .group_by(Client.id)
        .having(func.max(Appointment.date) < sixty_days_ago)
        .all()
    )

    sin_volver = [
        {
            "client": r[0],
            "days": (today - r[1]).days,
        }
        for r in rows
    ]

    return {
        "proximas": proximas_list,
        "sin_volver": sin_volver,
    }

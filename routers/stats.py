from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment
from sqlalchemy import func
from datetime import date

router = APIRouter(prefix="/stats", tags=["Stats"])


# --------------------------
# CAJA DEL DÍA / MES / AÑO
# --------------------------
@router.get("/caja")
def caja_stats(db: Session = Depends(get_db)):
    today = date.today()
    month_start = today.replace(day=1)
    year_start = today.replace(month=1, day=1)

    day_total = db.query(func.sum(Appointment.price)).filter(Appointment.date == today).scalar() or 0
    month_total = db.query(func.sum(Appointment.price)).filter(Appointment.date >= month_start).scalar() or 0
    year_total = db.query(func.sum(Appointment.price)).filter(Appointment.date >= year_start).scalar() or 0

    day_appointments = db.query(Appointment).filter(Appointment.date == today).count()

    avg_ticket = (month_total / day_appointments) if day_appointments > 0 else 0

    return {
        "day": day_total,
        "month": month_total,
        "year": year_total,
        "day_appointments": day_appointments,
        "avg_ticket": avg_ticket,
    }


# --------------------------
# CLIENTES
# --------------------------
@router.get("/clientes")
def clientes_stats(db: Session = Depends(get_db)):
    total = db.query(Client).count()

    hombres = db.query(Client).filter(Client.gender == "hombre").count()
    mujeres = db.query(Client).filter(Client.gender == "mujer").count()
    otros = db.query(Client).filter(Client.gender == "otro").count()

    today = date.today()
    month_start = today.replace(day=1)

    nuevos_mes = db.query(Client).filter(Client.created_at >= month_start).count()

    recurrentes_mes = (
        db.query(Client)
        .join(Appointment)
        .filter(Appointment.date >= month_start)
        .group_by(Client.id)
        .having(func.count(Appointment.id) > 1)
        .count()
    )

    return {
        "total": total,
        "hombres": hombres,
        "mujeres": mujeres,
        "otros": otros,
        "nuevos_mes": nuevos_mes,
        "recurrentes_mes": recurrentes_mes,
    }


# --------------------------
# OCUPACIÓN POR HORAS
# --------------------------
@router.get("/ocupacion/horas")
def ocupacion_horas(db: Session = Depends(get_db)):
    rows = (
        db.query(Appointment.time, func.count(Appointment.id))
        .group_by(Appointment.time)
        .order_by(Appointment.time)
        .all()
    )

    return [{"hour": str(r[0]), "count": r[1]} for r in rows]


# --------------------------
# SERVICIOS MÁS VENDIDOS
# --------------------------
@router.get("/servicios/top")
def servicios_top(db: Session = Depends(get_db)):
    rows = (
        db.query(Appointment.service, func.count(Appointment.id))
        .group_by(Appointment.service)
        .order_by(func.count(Appointment.id).desc())
        .limit(10)
        .all()
    )

    return [{"name": r[0], "count": r[1]} for r in rows]


# --------------------------
# PRODUCTOS MÁS VENDIDOS
# --------------------------
@router.get("/productos/top")
def productos_top(db: Session = Depends(get_db)):
    rows = (
        db.query(ProductSale.product, func.count(ProductSale.id))
        .group_by(ProductSale.product)
        .order_by(func.count(ProductSale.id).desc())
        .limit(10)
        .all()
    )

    return [{"name": r[0], "count": r[1]} for r in rows]

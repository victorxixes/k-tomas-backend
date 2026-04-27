from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from sqlalchemy.sql import func
from app.db.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    # Datos personales
    full_name = Column(String, nullable=False)
    dni = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=True)
    phone = Column(String, nullable=True)

    # Dirección
    direccion = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    piso = Column(String, nullable=True)
    puerta = Column(String, nullable=True)
    codigo_postal = Column(String, nullable=True)
    poblacion = Column(String, nullable=True)
    provincia = Column(String, nullable=True)

    # Consentimiento RGPD
    consentimiento_aceptado = Column(Boolean, default=False)
    consentimiento_firma_base64 = Column(Text, nullable=True)
    consentimiento_documento_url = Column(String, nullable=True)
    consentimiento_fecha = Column(DateTime, nullable=True)
    consentimiento_ip = Column(String, nullable=True)

    # Impagos
    impagos_total = Column(Integer, default=0)
    impagos_importe = Column(Float, default=0.0)
    impagos_detalle = Column(Text, nullable=True)

    # Histórico económico
    total_servicios = Column(Integer, default=0)
    total_facturado = Column(Float, default=0.0)
    ultimo_servicio_fecha = Column(DateTime, nullable=True)
    ultimo_servicio_importe = Column(Float, nullable=True)

    # Otros
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_visit = Column(DateTime, nullable=True)
    total_visits = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

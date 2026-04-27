from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ============================================================
# APPOINTMENT
# ============================================================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    client = Column(String, nullable=False)
    service = Column(String, nullable=False)
    stylist = Column(String, nullable=False)
    date = Column(String, nullable=False)
    time = Column(String, nullable=False)


# ============================================================
# CLIENT (FICHA COMPLETA)
# ============================================================
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)

    # Datos personales
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    dni = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    category = Column(String, nullable=True)

    # Datos de contacto
    phone = Column(String, nullable=True)
    phone_secondary = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    province = Column(String, nullable=True)

    # Sistema
    created_at = Column(String, nullable=False)

    # Relaciones
    fiscal_data = relationship("ClientFiscalData", back_populates="client", uselist=False)
    technical_sheet = relationship("ClientTechnicalSheet", back_populates="client", uselist=False)
    consent = relationship("ClientConsent", back_populates="client", uselist=False)
    hair_profiles = relationship("ClientHairProfile", back_populates="client")
    history = relationship("ClientHistory", back_populates="client")


# ============================================================
# DATOS FISCALES
# ============================================================
class ClientFiscalData(Base):
    __tablename__ = "client_fiscal_data"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    fiscal_name = Column(String, nullable=True)
    fiscal_id = Column(String, nullable=True)
    fiscal_email = Column(String, nullable=True)
    fiscal_address = Column(String, nullable=True)
    fiscal_city = Column(String, nullable=True)
    fiscal_postal_code = Column(String, nullable=True)
    fiscal_province = Column(String, nullable=True)

    client = relationship("Client", back_populates="fiscal_data")


# ============================================================
# FICHA TÉCNICA (PELUQUERÍA)
# ============================================================
class ClientTechnicalSheet(Base):
    __tablename__ = "client_technical_sheet"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    hair_type = Column(String, nullable=True)
    root_color = Column(String, nullable=True)

    client = relationship("Client", back_populates="technical_sheet")


# ============================================================
# CONSENTIMIENTOS
# ============================================================
class ClientConsent(Base):
    __tablename__ = "client_consent"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    consent_sms = Column(Boolean, default=False)
    consent_whatsapp = Column(Boolean, default=False)
    consent_email = Column(Boolean, default=False)
    lopd_signed = Column(Boolean, default=False)
    lopd_document_url = Column(String, nullable=True)

    client = relationship("Client", back_populates="consent")


# ============================================================
# PERFIL DE CABELLO (HISTÓRICO)
# ============================================================
class ClientHairProfile(Base):
    __tablename__ = "client_hair_profile"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    hair_type = Column(String, nullable=True)
    hair_length = Column(String, nullable=True)
    hair_color = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    client = relationship("Client", back_populates="hair_profiles")


# ============================================================
# HISTORIAL DE VISITAS
# ============================================================
class ClientHistory(Base):
    __tablename__ = "client_history"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))

    visit_date = Column(Date, nullable=False)
    service = Column(String, nullable=False)
    stylist = Column(String, nullable=True)
    amount = Column(Float, nullable=False)

    client = relationship("Client", back_populates="history")


# ============================================================
# HORARIOS
# ============================================================
class Horarios(Base):
    __tablename__ = "horarios"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(String, nullable=False)
    open_time = Column(String, nullable=False)
    close_time = Column(String, nullable=False)
    is_closed = Column(Integer, default=0)


# ============================================================
# SERVICE CONFIG
# ============================================================
class ServiceConfig(Base):
    __tablename__ = "service_config"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


# ============================================================
# PRODUCT (si ya existe en tu proyecto)
# ============================================================
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)


# ============================================================
# USER
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="empleado")

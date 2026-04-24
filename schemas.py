from pydantic import BaseModel
from datetime import date
from typing import Optional, List


# ============================================================
# APPOINTMENTS
# ============================================================
class AppointmentBase(BaseModel):
    client: str
    service: str
    stylist: str
    date: str
    time: str


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True


# ============================================================
# CLIENT — FICHA COMPLETA
# ============================================================

# ---------- Datos personales ----------
class ClientBase(BaseModel):
    name: str
    last_name: Optional[str] = None
    dni: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    category: Optional[str] = None

    # ---------- Datos de contacto ----------
    phone: Optional[str] = None
    phone_secondary: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    province: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True


# ============================================================
# DATOS FISCALES
# ============================================================
class ClientFiscalDataBase(BaseModel):
    fiscal_name: Optional[str] = None
    fiscal_id: Optional[str] = None
    fiscal_email: Optional[str] = None
    fiscal_address: Optional[str] = None
    fiscal_city: Optional[str] = None
    fiscal_postal_code: Optional[str] = None
    fiscal_province: Optional[str] = None


class ClientFiscalDataCreate(ClientFiscalDataBase):
    pass


class ClientFiscalData(ClientFiscalDataBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True


# ============================================================
# FICHA TÉCNICA (PELUQUERÍA)
# ============================================================
class ClientTechnicalSheetBase(BaseModel):
    hair_type: Optional[str] = None
    root_color: Optional[str] = None


class ClientTechnicalSheetCreate(ClientTechnicalSheetBase):
    pass


class ClientTechnicalSheet(ClientTechnicalSheetBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True


# ============================================================
# CONSENTIMIENTOS
# ============================================================
class ClientConsentBase(BaseModel):
    consent_sms: bool = False
    consent_whatsapp: bool = False
    consent_email: bool = False
    lopd_signed: bool = False
    lopd_document_url: Optional[str] = None


class ClientConsentCreate(ClientConsentBase):
    pass


class ClientConsent(ClientConsentBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True


# ============================================================
# PERFIL DE CABELLO (HISTÓRICO)
# ============================================================
class HairProfileBase(BaseModel):
    hair_type: Optional[str] = None
    hair_length: Optional[str] = None
    hair_color: Optional[str] = None
    allergies: Optional[str] = None
    notes: Optional[str] = None


class HairProfileCreate(HairProfileBase):
    pass  # client_id viene por la URL


class HairProfile(HairProfileBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True


# ============================================================
# HISTORIAL DE VISITAS
# ============================================================
class HistoryBase(BaseModel):
    visit_date: date
    service: str
    stylist: Optional[str] = None
    amount: float


class HistoryCreate(HistoryBase):
    pass  # client_id viene por la URL


class History(HistoryBase):
    id: int
    client_id: int

    class Config:
        orm_mode = True


# ============================================================
# SERVICES
# ============================================================
class ServiceBase(BaseModel):
    name: str
    duration: int
    price: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int

    class Config:
        orm_mode = True


# ============================================================
# PRODUCTS
# ============================================================
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


# ============================================================
# SCHEDULE
# ============================================================
class ScheduleBase(BaseModel):
    day: str
    open_time: str
    close_time: str
    is_closed: int


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int

    class Config:
        orm_mode = True

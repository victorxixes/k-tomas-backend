from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class ClientBase(BaseModel):
    full_name: str
    dni: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    direccion: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    puerta: Optional[str] = None
    codigo_postal: Optional[str] = None
    poblacion: Optional[str] = None
    provincia: Optional[str] = None

    consentimiento_aceptado: bool = False
    notes: Optional[str] = None

class ClientCreate(ClientBase):
    pass

class ClientUpdate(ClientBase):
    is_active: Optional[bool] = None

class ClientOut(ClientBase):
    id: int
    impagos_total: int
    impagos_importe: float
    total_servicios: int
    total_facturado: float
    last_visit: Optional[datetime] = None
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}

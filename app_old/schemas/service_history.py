from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ServiceHistoryBase(BaseModel):
    client_id: int
    service_name: str
    price: float
    employee: Optional[str] = None
    paid: bool = True
    notes: Optional[str] = None

class ServiceHistoryCreate(ServiceHistoryBase):
    pass

class ServiceHistoryOut(ServiceHistoryBase):
    id: int
    date: datetime

    model_config = {"from_attributes": True}

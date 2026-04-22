from pydantic import BaseModel

# -------------------------
# APPOINTMENTS
# -------------------------
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


# -------------------------
# CLIENTS
# -------------------------
class ClientBase(BaseModel):
    name: str
    phone: str | None = None
    email: str | None = None
    created_at: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    class Config:
        orm_mode = True


# -------------------------
# SERVICES
# -------------------------
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


# -------------------------
# PRODUCTS
# -------------------------
class ProductBase(BaseModel):
    name: str
    price: int
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    class Config:
        orm_mode = True


# -------------------------
# SCHEDULE
# -------------------------
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

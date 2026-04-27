from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class ServiceHistory(Base):
    __tablename__ = "service_history"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    service_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    employee = Column(String, nullable=True)
    date = Column(DateTime, server_default=func.now())
    paid = Column(Boolean, default=True)
    notes = Column(String, nullable=True)

    client = relationship("Client", backref="services")

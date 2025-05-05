from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    reserved_guyok = Column(String(255), index=True, nullable=False) # 길이 명시 권장
    # MySQL 5.7+ JSON 타입 사용
    seat_identifiers = Column(JSON, nullable=False)
    reservation_time = Column(DateTime(timezone=True), server_default=func.now())

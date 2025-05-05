from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# --- Reservation ---
class ReservationBase(BaseModel):
    reserved_guyok: str = Field(..., example="A구역")
    # 예약 시 최소 1개 좌석 필요
    seat_identifiers: List[str] = Field(..., min_items=1, example=["A1", "A2"])

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase): # 응답 시 사용할 스키마
    id: int
    reservation_time: datetime

    class Config:
        from_attributes = True # Pydantic V2 (orm_mode 대체)

# --- WebSocket Message ---
class WebSocketMessage(BaseModel):
    type: str = Field(..., example="reservation_update")
    # 현재 예약된 모든 좌석 식별자 목록
    data: List[str] = Field(..., example=["A1", "A2", "B3"])
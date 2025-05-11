from pydantic import BaseModel, Field
from typing import List, Dict, Any
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

# --- WebSocket Message Schemas ---
class SeatDetailSchema(BaseModel):
    """WebSocket 메시지 내 개별 좌석 상세 정보 스키마"""
    id: str # 프론트엔드에서 좌석 객체의 id로 사용 (seat_identifier와 동일값)
    seat_identifier: str

class ReservationForWebSocket(BaseModel):
    """WebSocket 메시지에서 사용될 개별 예약 정보 스키마"""
    id: int # 예약 ID
    reserved_guyok: str
    seats: List[SeatDetailSchema]

class WebSocketMessage(BaseModel):
    type: str = Field(..., example="reservation_update")
    # data: List[str] = Field(..., example=["A1", "A2", "B3"]) # 기존 타입
    data: List[ReservationForWebSocket] # 새로운 타입: 예약 상세 정보 리스트
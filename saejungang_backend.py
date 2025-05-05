import fastapi
from fastapi import WebSocket, WebSocketDisconnect, HTTPException, Body
from typing import List, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware

# Pydantic 모델 정의 (예시)
from pydantic import BaseModel

# 모듈 임포트 (상대 경로 또는 절대 경로 설정 필요 시 sys.path 수정)
import database
import models
from api import reservations # API 라우터
from ws import router as ws_router # WebSocket 라우터

class Seat(BaseModel):
    id: int
    identifier: str # 예: "A1", "B5" 등 좌석 고유 식별자
    is_reserved: bool = False
    reserved_guyok: str

# FastAPI 앱 인스턴스 생성
app = fastapi.FastAPI(
    title="새중앙 좌석 예약 시스템 API",
    description="FastAPI와 WebSocket을 이용한 좌석 예약 백엔드",
    version="0.1.0"
)

# --- CORS 미들웨어 설정 (필요 시) ---
# origins = [
#     "http://localhost",
#     "http://localhost:3000", # 예: 프론트엔드 개발 서버 주소
#     # 실제 배포 환경의 프론트엔드 주소 추가
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# --- 데이터 저장소 (간단한 인메모리 예시) ---
# 실제 애플리케이션에서는 데이터베이스를 사용해야 합니다.
seats_db: Dict[int, Seat] = {
    1: Seat(id=1, identifier="A1"),
    2: Seat(id=2, identifier="A2"),
    3: Seat(id=3, identifier="B1"),
    4: Seat(id=4, identifier="B2", is_reserved=True), # 예시: 이미 예약된 좌석
    5: Seat(id=5, identifier="C1"),
}
next_seat_id = 6 # 다음 좌석 ID 관리를 위한 변수 (예시)

# --- WebSocket 연결 관리 ---
active_connections: List[WebSocket] = []

async def notify_clients():
    """모든 연결된 클라이언트에게 현재 좌석 상태를 알립니다."""
    seats_data = [seat.dict() for seat in seats_db.values()]
    for connection in active_connections:
        try:
            # .dict() 대신 .model_dump() 사용 (Pydantic v2 권장)
            await connection.send_json({"type": "seat_update", "data": [s.model_dump() for s in seats_db.values()]})
        except Exception:
            # 연결이 끊어진 경우 등 예외 처리
            pass

# --- API 엔드포인트 ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"Client connected: {websocket.client}")
    # 연결 시 현재 좌석 상태 전송
    await notify_clients()
    try:
        while True:
            # 클라이언트로부터 메시지 수신 대기 (필요에 따라 로직 추가)
            data = await websocket.receive_text()
            print(f"Message from {websocket.client}: {data}")
            # 예시: 수신 메시지에 따라 특정 동작 수행 후 상태 업데이트 알림
            # await notify_clients()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"WebSocket Error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)

@app.get("/reserve-test")
async def reservation_test():
    # 실제 예약 로직 대신 간단한 메시지 반환 (seatService.reservation() 대체)
    print("Reservation test endpoint called")
    return {"message": "Reservation test successful!"}

@app.get("/seats")
async def get_all_seats():
    # 모든 좌석 정보 반환 (seatService.getAllSeats() 대체)
    print("Get all seats endpoint called")
    return list(seats_db.values())

@app.get("/seats/{id}")
async def get_seat_by_id(id: int):
    # 특정 ID의 좌석 정보 반환 (seatService.getSeatById() 대체)
    print(f"Get seat by ID endpoint called with id: {id}")
    seat = seats_db.get(id)
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    return seat

@app.put("/seats/reserve")
async def reserve_seats(seat_identifiers: List[str] = Body(...)):
    # 여러 좌석 예약 처리 (seatService.reserveSeats() 대체)
    print(f"Reserve seats endpoint called with identifiers: {seat_identifiers}")
    reserved_seats = []
    not_found_seats = []
    already_reserved_seats = []

    updated = False
    for identifier in seat_identifiers:
        found_seat: Optional[Seat] = None
        for seat in seats_db.values():
            if seat.identifier == identifier:
                found_seat = seat
                break

        if found_seat is None:
            not_found_seats.append(identifier)
        elif found_seat.is_reserved:
            already_reserved_seats.append(identifier)
        else:
            found_seat.is_reserved = True
            reserved_seats.append(found_seat)
            updated = True

    if not_found_seats or already_reserved_seats:
        details = {}
        if not_found_seats:
            details["not_found"] = not_found_seats
        if already_reserved_seats:
            details["already_reserved"] = already_reserved_seats
        # 일부만 성공했더라도 200 OK를 반환하고 상세 내역을 body에 포함하거나,
        # 상태 코드 400 또는 409 등을 사용하고 실패 사유를 명확히 전달할 수 있습니다.
        # 여기서는 409 Conflict 와 함께 상세 정보를 반환합니다.
        # 에러 발생 시 모든 예약을 롤백하는 로직은 추가되지 않았습니다.
        if updated:
            await notify_clients() # 일부 성공 시에도 상태 변경 알림
        raise HTTPException(
            status_code=409, # Conflict
            detail={"message": "Some seats could not be reserved.", **details}
        )

    if updated:
        await notify_clients() # 좌석 상태 변경 알림

    return {"message": "Seats reserved successfully", "reserved_seats": [s.identifier for s in reserved_seats]}

@app.put("/seats/{id}/cancel")
async def cancel_reserve_seat(id: int):
    # 특정 ID 좌석 예약 취소 (seatService.cancelReserveSeat() 대체)
    print(f"Cancel reserve seat endpoint called with id: {id}")
    seat = seats_db.get(id)
    if seat is None:
        raise HTTPException(status_code=404, detail="Seat not found")
    if not seat.is_reserved:
        raise HTTPException(status_code=400, detail="Seat is not currently reserved")

    seat.is_reserved = False
    await notify_clients() # 좌석 상태 변경 알림
    return {"message": f"Reservation for seat {seat.identifier} (ID: {id}) cancelled successfully"}

# --- 라우터 포함 ---
app.include_router(reservations.router) # API 엔드포인트
app.include_router(ws_router.router)   # WebSocket 엔드포인트

# --- 기본 경로 ---
@app.get("/")
def read_root():
    return {"message": "Saejungang Reservation Backend is running!"}

# --- 서버 실행 (uvicorn 사용 시) ---
# 터미널에서: uvicorn saejungang_backend:app --reload --host 0.0.0.0 --port 8000
# (또는 main:app, 파일 이름에 따라)


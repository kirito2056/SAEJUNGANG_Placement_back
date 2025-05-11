from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from typing import List

from ws.manager import manager # WebSocket 매니저
import crud
import schemas
from database import get_db # DB 세션 의존성 주입

router = APIRouter(
    prefix="/ws",
    tags=["websocket"]
)

@router.websocket("") # /ws 경로
async def websocket_endpoint(
    websocket: WebSocket,
    db: Session = Depends(get_db) # DB 세션 주입 (연결 시 초기 데이터 조회용)
):
    await manager.connect(websocket)
    try:
        # 1. 연결 시 현재 예약된 모든 "예약 정보" 목록 전송
        reservations_orm = crud.get_reservations(db, skip=0, limit=1000) # 모든 예약 가져오기 (limit 충분히 크게)
        
        payload_data: List[schemas.ReservationForWebSocket] = []
        for r_orm in reservations_orm:
            seats_details = [
                schemas.SeatDetailSchema(id=sid, seat_identifier=sid) 
                for sid in r_orm.seat_identifiers
            ]
            payload_data.append(
                schemas.ReservationForWebSocket(
                    id=r_orm.id,
                    reserved_guyok=r_orm.reserved_guyok,
                    seats=seats_details
                )
            )

        await websocket.send_text(
            schemas.WebSocketMessage(type="initial_state", data=payload_data).model_dump_json()
        )

        # 2. 클라이언트로부터 메시지 수신 대기 (필요 시 로직 추가)
        while True:
            data = await websocket.receive_text()
            print(f"Message received from {websocket.client}: {data}")
            # 여기서 클라이언트의 특정 요청을 처리하고 응답하거나, 상태 변경 후 브로드캐스트 할 수 있습니다.
            # 예: await manager.broadcast(schemas.WebSocketMessage(type="some_update", data=new_payload))

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {websocket.client} disconnected (WebSocketDisconnect)")
    except Exception as e:
        # 예상치 못한 오류 발생 시 연결 종료 처리
        print(f"WebSocket Error for {websocket.client}: {e}")
        manager.disconnect(websocket)
        # 필요한 경우 에러 메시지 전송 시도 (연결이 아직 유효하다면)
        try:
             await websocket.close(code=1011) # Internal Error
        except:
             pass # 이미 닫혔을 수 있음

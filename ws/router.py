from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from ws.manager import manager # 명시적으로 ws.manager 사용
import crud
import schemas
from database import get_db

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
        # 1. 연결 시 현재 예약된 모든 좌석 목록 전송
        current_reserved_seats = crud.get_all_reserved_seat_identifiers(db)
        await websocket.send_text(
            schemas.WebSocketMessage(type="initial_state", data=current_reserved_seats).model_dump_json()
        )

        # 2. 클라이언트로부터 메시지 수신 대기 (필요 시 로직 추가)
        while True:
            data = await websocket.receive_text()
            # 예시: 클라이언트가 메시지를 보내는 경우 처리 로직
            print(f"Message received from {websocket.client}: {data}")
            # 단순 에코 예시
            # await websocket.send_text(f"Message text was: {data}")
            # 특정 요청 처리 후 manager.broadcast() 호출 등 가능

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

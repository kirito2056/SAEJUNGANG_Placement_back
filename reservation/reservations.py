from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

# from .. import crud, schemas, models # 상위 폴더 참조 -> 변경
import crud
import schemas
import models
# from ..database import get_db # DB 세션 의존성 주입 -> 변경
from database import get_db
# from ..ws.manager import manager # WebSocket 매니저 -> 변경
from ws.manager import manager

router = APIRouter(
    prefix="/reservations", # 이 라우터의 모든 경로는 /reservations 로 시작
    tags=["reservations"]  # API 문서 그룹화 태그
)

# --- 의존성 주입 ---
# WebSocket 매니저를 직접 Depends로 주입할 필요는 없으나,
# 필요하다면 함수 형태로 만들어 Depends 사용 가능
# def get_ws_manager():
#    return manager

# --- API 엔드포인트 ---

@router.post("/", response_model=schemas.ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_new_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db)
    # ws_manager: ConnectionManager = Depends(get_ws_manager) # 필요 시
):
    """
    새로운 좌석 예약을 생성합니다.
    - `reserved_guyok`: 예약하는 구역 이름 (예: "본당 A구역")
    - `seat_identifiers`: 예약할 좌석 식별자 목록 (예: ["A1", "A2"])
    이미 예약된 좌석이 포함되어 있으면 409 Conflict 에러를 반환합니다.
    성공 시 예약 정보를 반환하고 WebSocket 클라이언트에게 업데이트를 알립니다.
    """
    try:
        created_reservation = crud.create_reservation(db=db, reservation=reservation)
        # 예약 성공 후 모든 클라이언트에게 최신 예약 좌석 목록 알림
        all_reserved_seats = crud.get_all_reserved_seat_identifiers(db)
        await manager.broadcast(schemas.WebSocketMessage(type="reservation_update", data=all_reserved_seats))
        # Pydantic 모델로 변환하여 반환 (자동 변환되지만 명시적으로)
        # return schemas.ReservationResponse.from_orm(created_reservation) # Pydantic V1
        return schemas.ReservationResponse.model_validate(created_reservation) # Pydantic V2
    except ValueError as e:
        # crud.create_reservation 에서 발생시킨 중복 예약 에러 처리
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        # 기타 예상치 못한 오류 처리
        print(f"Error creating reservation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the reservation."
        )

@router.get("/", response_model=List[schemas.ReservationResponse])
def read_reservations(
    reserved_guyok: Optional[str] = None, # 구역명 필터 (선택적 쿼리 파라미터)
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    예약 목록을 조회합니다. (페이징 및 구역명 필터링 가능)
    - `reserved_guyok` 쿼리 파라미터 제공 시 해당 구역의 예약만 반환합니다.
    - 제공하지 않으면 모든 예약을 반환합니다.
    """
    if reserved_guyok:
        reservations = crud.get_reservations_by_guyok(db, reserved_guyok=reserved_guyok)
        # 페이징은 구역별 조회 시에는 적용하지 않거나, 별도 로직 추가 필요
        # 여기서는 구역별 조회 시 skip/limit 무시하고 전부 반환
    else:
        reservations = crud.get_reservations(db, skip=skip, limit=limit)

    return reservations

@router.get("/seats", response_model=List[str])
def read_reserved_seats(db: Session = Depends(get_db)):
    """
    현재 예약된 모든 좌석 식별자 목록을 반환합니다.
    """
    return crud.get_all_reserved_seat_identifiers(db=db)


@router.delete("/seats/{seat_identifier}", status_code=status.HTTP_200_OK)
async def cancel_seat_reservation(
    seat_identifier: str,
    db: Session = Depends(get_db)
    # ws_manager: ConnectionManager = Depends(get_ws_manager) # 필요 시
):
    """
    특정 좌석 식별자의 예약을 취소합니다.
    해당 좌석이 포함된 예약을 찾아 좌석을 제거하거나, 마지막 좌석이면 예약을 삭제합니다.
    성공 시 메시지를 반환하고 WebSocket 클라이언트에게 업데이트를 알립니다.
    예약된 좌석이 아니면 404 Not Found 에러를 반환합니다.
    """
    result = crud.delete_reservation_by_seat(db=db, seat_identifier=seat_identifier)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seat '{seat_identifier}' is not currently reserved or reservation not found."
        )

    # 예약 취소 성공 후 모든 클라이언트에게 최신 예약 좌석 목록 알림
    all_reserved_seats = crud.get_all_reserved_seat_identifiers(db)
    await manager.broadcast(schemas.WebSocketMessage(type="reservation_update", data=all_reserved_seats))

    if result["deleted_reservation"]:
        return {"message": f"Reservation containing seat '{seat_identifier}' (ID: {result['reservation_id']}) was deleted as it was the last seat."}
    else:
        return {"message": f"Seat '{seat_identifier}' was removed from reservation ID {result['reservation_id']}."}

# 필요 시 특정 예약 조회, 수정 등 엔드포인트 추가 가능
# @router.get("/{reservation_id}", response_model=schemas.ReservationResponse)
# ...
# @router.put("/{reservation_id}", response_model=schemas.ReservationResponse)
# ...

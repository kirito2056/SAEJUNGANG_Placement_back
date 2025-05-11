# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func # JSON 함수 사용 위해 추가 (선택적)
import models # 변경
import schemas # 변경
from typing import List, Optional, Dict, Any

# --- Reservation CRUD ---

def get_reservation(db: Session, reservation_id: int) -> Optional[models.Reservation]:
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

def get_reservations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Reservation]:
    return db.query(models.Reservation).offset(skip).limit(limit).all()

def get_all_reserved_seat_identifiers(db: Session) -> List[str]:
    """현재 예약된 모든 좌석 식별자 목록을 반환합니다."""
    reservations = db.query(models.Reservation.seat_identifiers).all()
    reserved_seats = set()
    for seats_list in reservations:
        # seats_list는 (['A1', 'A2'],) 형태의 튜플일 수 있음
        if seats_list and isinstance(seats_list[0], list):
            reserved_seats.update(seats_list[0])
    return sorted(list(reserved_seats))

def create_reservation(db: Session, reservation: schemas.ReservationCreate) -> models.Reservation:
    """새로운 예약을 생성합니다. 좌석 중복 시 ValueError 발생"""
    existing_reserved_seats = set(get_all_reserved_seat_identifiers(db))
    requested_seats = set(reservation.seat_identifiers)

    already_reserved = requested_seats.intersection(existing_reserved_seats)
    if already_reserved:
        raise ValueError(f"Seats already reserved: {', '.join(sorted(list(already_reserved)))}")

    db_reservation = models.Reservation(
        reserved_guyok=reservation.reserved_guyok,
        seat_identifiers=reservation.seat_identifiers
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def delete_reservation_by_seat(db: Session, seat_identifier: str) -> Optional[Dict[str, Any]]:
    """
    지정된 좌석 식별자를 포함하는 예약을 찾아 해당 좌석을 제거합니다.
    만약 해당 좌석이 예약의 마지막 좌석이었다면 예약 자체를 삭제합니다.
    변경 사항이 있으면 {'seat_identifier': str, 'reservation_id': int, 'deleted_reservation': bool} 반환, 없으면 None 반환.
    """
    # MySQL 5.7+ JSON_CONTAINS 또는 JSON_SEARCH 사용 가능
    # 여기서는 간단하게 Python 로직으로 처리
    reservations_with_seat = db.query(models.Reservation).filter(
        # SQLAlchemy는 JSON 컬럼에 대한 기본적인 연산자를 제공할 수 있음
        # 하지만 복잡한 쿼리는 DB 함수 직접 사용 필요
        # 여기서는 일단 모든 예약을 가져와 필터링 (데이터 양 많으면 비효율적)
        models.Reservation.seat_identifiers.isnot(None) # 혹시 모를 NULL 방지
    ).all()

    target_reservation: Optional[models.Reservation] = None
    for res in reservations_with_seat:
        if isinstance(res.seat_identifiers, list) and seat_identifier in res.seat_identifiers:
            target_reservation = res
            break

    if not target_reservation:
        return None # 해당 좌석을 포함한 예약 없음

    original_reservation_id = target_reservation.id
    updated_seats = [s for s in target_reservation.seat_identifiers if s != seat_identifier]
    deleted_reservation = False

    if not updated_seats:
        # 마지막 남은 좌석이면 예약 삭제
        db.delete(target_reservation)
        deleted_reservation = True
    else:
        # 좌석 목록 업데이트
        target_reservation.seat_identifiers = updated_seats
        db.add(target_reservation) # 변경사항 반영

    db.commit()

    return {
        "seat_identifier": seat_identifier,
        "reservation_id": original_reservation_id,
        "deleted_reservation": deleted_reservation
    }

# --- 구역별 예약 조회 함수 추가 ---
def get_reservations_by_guyok(db: Session, reserved_guyok: str) -> List[models.Reservation]:
    """특정 구역명(reserved_guyok)으로 예약 목록을 조회합니다."""
    return db.query(models.Reservation).filter(models.Reservation.reserved_guyok == reserved_guyok).all()

# 구역별 예약 조회 등 추가 CRUD 함수 필요 시 여기에 정의
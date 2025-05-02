package saejungang.saejungang_place_reservation.resarvation.service;

import org.springframework.http.ResponseEntity;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;

import java.util.List;

public interface SeatService {
    ResponseEntity<Object> reservation(); // 예시 메소드, 실제 로직에 맞게 수정 또는 제거

    ResponseEntity<Object> getAllSeats();

    ResponseEntity<SeatEntity> getSeatById(Long Id);

    ResponseEntity<Object> reserveSeat(List<SeatEntity> seatEntityList);

    ResponseEntity<Object> reserveSeats(List<String> seatIdentifiers);

    ResponseEntity<Object> cancelReserveSeat(Long seatId);

}
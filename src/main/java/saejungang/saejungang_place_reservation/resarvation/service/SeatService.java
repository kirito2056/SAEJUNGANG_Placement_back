package saejungang.saejungang_place_reservation.resarvation.service;

import org.springframework.http.ResponseEntity;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;

import java.util.List;

public interface SeatService {
    ResponseEntity<Object> reservation();

    ResponseEntity<Object> getAllSeats();

    ResponseEntity<Object> getSeatById(Long Id);

    ResponseEntity<Object> reserveSeat(List<SeatEntity> seatEntityList);

    ResponseEntity<Object> cancelReserveSeat(Long SeatId);
}

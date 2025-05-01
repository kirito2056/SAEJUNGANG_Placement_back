package saejungang.saejungang_place_reservation.resarvation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

import java.util.List;

@RestController
@RequestMapping("/place")
public class SeatController {
    SeatService placeService;

    @PostMapping("/reserve")
    public ResponseEntity<Object> reservation() {
        return placeService.reservation();
    }

    @PutMapping("/reservation")
    public ResponseEntity<Object> reserve_seats(List<SeatEntity> seatEntityList) {
        return ResponseEntity.ok(placeService.reserveSeat(seatEntityList));
    }
}

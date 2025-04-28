package saejungang.saejungang_place_reservation.resarvation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

@RestController
@RequestMapping("/place")
public class SeatController {
    SeatService placeService;

    @PostMapping("/reserve")
    public ResponseEntity<Object> reservation() {
        return placeService.reservation();
    }
}

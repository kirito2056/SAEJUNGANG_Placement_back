package saejungang.saejungang_place_reservation.resarvation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import saejungang.saejungang_place_reservation.resarvation.service.PlaceService;

@RestController
@RequestMapping("/place")
public class PlaceController {
    PlaceService placeService;

    @PostMapping("/reserve")
    public ResponseEntity<Object> reservation() {
        return placeService.reservation();
    }
}

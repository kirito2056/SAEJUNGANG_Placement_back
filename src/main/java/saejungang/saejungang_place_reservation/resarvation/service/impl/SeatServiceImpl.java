package saejungang.saejungang_place_reservation.resarvation.service.impl;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

@Service
public class SeatServiceImpl implements SeatService {
    @Override
    public ResponseEntity<Object> reservation() {
        return ResponseEntity.ok("Hello World");
    }
}

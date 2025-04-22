package saejungang.saejungang_place_reservation.resarvation.service.impl;

import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;

@Service
public class PlaceServiceImpl implements saejungang.saejungang_place_reservation.resarvation.service.PlaceService {
    @Override
    public ResponseEntity<Object> reservation() {
        return ResponseEntity.ok("Hello World");
    }
}

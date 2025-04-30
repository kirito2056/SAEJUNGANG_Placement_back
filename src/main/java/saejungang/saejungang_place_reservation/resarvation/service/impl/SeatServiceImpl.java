package saejungang.saejungang_place_reservation.resarvation.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;
import saejungang.saejungang_place_reservation.resarvation.repository.SeatRepository;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class SeatServiceImpl implements SeatService {

    private final SeatRepository seatRepository;
    Map<String, Object> returnData = new HashMap<>();

    @Autowired // 생성자 주입
    public SeatServiceImpl(SeatRepository seatRepository) {
        this.seatRepository = seatRepository;
    }
    @Override
    public ResponseEntity<Object> reservation() {
        return ResponseEntity.ok("Hello World");
    }

    @Override
    public ResponseEntity<Object> getAllSeats() {
        returnData.put("seats", seatRepository.findAllSeats());
        return ResponseEntity.ok(returnData);
    }

    @Override
    public ResponseEntity<Object> getSeatById(Long Id) {
        return null;
    }

    @Override
    public ResponseEntity<Object> reserveSeat(List<SeatEntity> seatEntityList) {


        return null;
    }

    @Override
    public ResponseEntity<Object> cancelReserveSeat(Long SeatId) {
        return null;
    }
}

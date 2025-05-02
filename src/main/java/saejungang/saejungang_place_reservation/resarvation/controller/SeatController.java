package saejungang.saejungang_place_reservation.resarvation.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

import java.util.List;

@RestController
@RequestMapping("/place")
public class SeatController {
    private final SeatService seatService;

    // 생성자 주입 (Autowired 생략 가능)
    public SeatController(SeatService seatService) {
        this.seatService = seatService;
    }

    @GetMapping("/reserve-test")
    public ResponseEntity<Object> reservationTest() {
        return seatService.reservation();
    }

    @GetMapping("/seats")
    public ResponseEntity<Object> getAllSeats() {
        return seatService.getAllSeats();
    }

    @GetMapping("/seats/{id}")
    public ResponseEntity<SeatEntity> getSeatById(@PathVariable("id") Long id) {
        return seatService.getSeatById(id);
    }

    @PutMapping("/seats/reserve")
    public ResponseEntity<Object> reserveSeats(@RequestBody List<String> seatIdentifiers) {
        return seatService.reserveSeats(seatIdentifiers);
    }

    @PutMapping("/seats/{id}/cancel")
    public ResponseEntity<Object> cancelReserveSeat(@PathVariable("id") Long id) {
        return seatService.cancelReserveSeat(id);
    }
}
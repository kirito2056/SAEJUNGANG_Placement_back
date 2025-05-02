package saejungang.saejungang_place_reservation.resarvation.service.impl;

import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;
import saejungang.saejungang_place_reservation.resarvation.repository.SeatRepository;
import saejungang.saejungang_place_reservation.resarvation.service.SeatService;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class SeatServiceImpl implements SeatService {

    private final SeatRepository seatRepository;

    @Autowired
    public SeatServiceImpl(SeatRepository seatRepository) {
        this.seatRepository = seatRepository;
    }

    @Override
    public ResponseEntity<Object> reservation() {
        return ResponseEntity.ok("Reservation endpoint reached.");
    }

    @Override
    public ResponseEntity<Object> getAllSeats() {
        return ResponseEntity.ok(seatRepository.findAll());
    }

    @Override
    public ResponseEntity<SeatEntity> getSeatById(Long id) {
        return seatRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @Override
    public ResponseEntity<Object> reserveSeat(List<SeatEntity> seatEntityList) {
        // 명시적으로 아직 구현되지 않았음을 알림
        return ResponseEntity.status(HttpStatus.NOT_IMPLEMENTED)
                .body("Not implemented. Use reserveSeats instead.");
    }

    @Override
    @Transactional
    public ResponseEntity<Object> reserveSeats(List<String> seatIdentifiers) {
        if (seatIdentifiers == null || seatIdentifiers.isEmpty()) {
            return ResponseEntity.badRequest().body("예약하려면 좌석 ID가 필요합니다.");
        }

        List<SeatEntity> seatsToReserve = seatRepository.findByFloorAndRowIn(seatIdentifiers);

        List<String> foundIdentifiers = seatsToReserve.stream()
                .map(SeatEntity::getFloor_and_row)
                .collect(Collectors.toList());

        List<String> notFoundIdentifiers = seatIdentifiers.stream()
                .filter(id -> !foundIdentifiers.contains(id))
                .collect(Collectors.toList());

        if (!notFoundIdentifiers.isEmpty()) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body("다음 좌석을 찾을 수 없습니다: " + notFoundIdentifiers);
        }

        List<String> alreadyReserved = seatsToReserve.stream()
                .filter(SeatEntity::isReserved)
                .map(SeatEntity::getFloor_and_row)
                .collect(Collectors.toList());

        if (!alreadyReserved.isEmpty()) {
            return ResponseEntity.status(HttpStatus.CONFLICT)
                    .body("다음 좌석은 이미 예약되어 있습니다: " + alreadyReserved);
        }

        seatsToReserve.forEach(seat -> seat.setReserved(true));
        seatRepository.saveAll(seatsToReserve);

        return ResponseEntity.ok(seatsToReserve);
    }

    @Override
    @Transactional
    public ResponseEntity<Object> cancelReserveSeat(Long seatId) {
        Optional<SeatEntity> seatOptional = seatRepository.findById(seatId);

        if (seatOptional.isEmpty()) {
            return ResponseEntity.ok("");
        }

        SeatEntity seatToCancel = seatOptional.get();

        if (!seatToCancel.isReserved()) {
            return ResponseEntity.badRequest().body("Seat " + seatToCancel.getFloor_and_row() + " is not currently reserved.");
        }

        seatToCancel.setReserved(false);

        seatRepository.save(seatToCancel);

        return ResponseEntity.ok().body("Seat " + seatToCancel.getFloor_and_row() + " reservation cancelled successfully.");
    }
}

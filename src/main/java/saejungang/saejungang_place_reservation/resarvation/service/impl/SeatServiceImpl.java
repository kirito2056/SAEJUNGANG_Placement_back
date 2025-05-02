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

import static org.springframework.http.ResponseEntity.notFound;

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
        List<SeatEntity> seats = seatRepository.findAll();
        return ResponseEntity.ok(seats);
    }

    @Override
    public ResponseEntity<SeatEntity> getSeatById(Long id) {
        Optional<SeatEntity> seatOptional = seatRepository.findById(id);

        return seatOptional.map(seat -> ResponseEntity.ok().body(seat))
                .orElseGet(() -> notFound().build());
    }

    @Override
    public ResponseEntity<Object> reserveSeat(List<SeatEntity> seatEntityList) {
        return null;
    }

    @Override
    @Transactional
    public ResponseEntity<Object> reserveSeats(List<String> seatIdentifiers) {
        if (seatIdentifiers == null || seatIdentifiers.isEmpty()) {
            return ResponseEntity.badRequest().body("Reservation request must contain seat identifiers.");
        }

        List<SeatEntity> seatsToReserve = seatRepository.findByFloorAndRowIn(seatIdentifiers);

        if (seatsToReserve.size() != seatIdentifiers.size()) {
            List<String> foundIdentifiers = seatsToReserve.stream()
                    .map(SeatEntity::getFloor_and_row)
                    .collect(Collectors.toList());
            List<String> notFoundIdentifiers = seatIdentifiers.stream()
                    .filter(id -> !foundIdentifiers.contains(id))
                    .collect(Collectors.toList());
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Some seats not found: " + notFoundIdentifiers);
        }

        List<SeatEntity> alreadyReservedSeats = seatsToReserve.stream()
                .filter(SeatEntity::isReserved)
                .collect(Collectors.toList());

        if (!alreadyReservedSeats.isEmpty()) {
            List<String> reservedIdentifiers = alreadyReservedSeats.stream()
                    .map(SeatEntity::getFloor_and_row)
                    .collect(Collectors.toList());
            return ResponseEntity.status(HttpStatus.CONFLICT).body("Some seats are already reserved: " + reservedIdentifiers);
        }

        seatsToReserve.forEach(seat -> seat.setReserved(true));

        seatRepository.saveAll(seatsToReserve);

        return ResponseEntity.ok().body(seatsToReserve);
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
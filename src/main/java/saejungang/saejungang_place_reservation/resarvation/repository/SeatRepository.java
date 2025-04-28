package saejungang.saejungang_place_reservation.resarvation.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;

@Repository
public interface SeatRepository extends JpaRepository<SeatEntity, Long> {
}

package saejungang.saejungang_place_reservation.resarvation.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import saejungang.saejungang_place_reservation.resarvation.entity.PlaceEntity;

@Repository
public interface PlaceRepository extends JpaRepository<PlaceEntity, Long> {
}

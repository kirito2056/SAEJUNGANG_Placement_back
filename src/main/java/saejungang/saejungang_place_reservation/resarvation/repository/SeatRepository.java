package saejungang.saejungang_place_reservation.resarvation.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param; // @Param 임포트
import org.springframework.stereotype.Repository;
import saejungang.saejungang_place_reservation.resarvation.entity.SeatEntity;

import java.util.List;
import java.util.Optional;

@Repository
public interface SeatRepository extends JpaRepository<SeatEntity, Long> {
    @Query("SELECT s FROM SeatEntity s WHERE s.floor_and_row IN :seatIdentifiers")
    List<SeatEntity> findByFloorAndRowIn(@Param("seatIdentifiers") List<String> seatIdentifiers);

    @Query("SELECT s FROM SeatEntity s WHERE s.floor_and_row = :floorAndRow")
    Optional<SeatEntity> findByFloorAndRow(@Param("floorAndRow") String floorAndRow); // @Param 어노테이션 추가
}
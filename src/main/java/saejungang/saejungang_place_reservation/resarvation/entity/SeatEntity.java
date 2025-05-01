package saejungang.saejungang_place_reservation.resarvation.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.*;

@Entity
@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class SeatEntity {

    @Id
    @Column(unique = true, nullable = false)
    @GeneratedValue()
    private Long seatId;

    @Column(nullable = false, unique = true)
    private String floor_and_row;

    @Column
    private boolean reserved = false;
}

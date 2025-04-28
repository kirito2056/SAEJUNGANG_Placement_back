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
    private Long placeId;

    @Column(nullable = false, unique = true)
    private String coordinate;

    @Column
    private boolean reserved = false;
}

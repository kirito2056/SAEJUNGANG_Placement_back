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
public class PlaceEntity {

    @Id
    @Column(unique = true, nullable = false)
    @GeneratedValue()
    private Long placeId;

    @Column
    private boolean reserved = false;

    @Column(nullable = false)
    private short coordinate;
}

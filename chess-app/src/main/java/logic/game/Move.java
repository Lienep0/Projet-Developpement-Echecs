/**
 * Classe permettant de définir un déplacement (stocke un point d'arrivée et un point de départ).
 */

package logic.game;

public class Move {

    public final Position start;
    public final Position end;

    public Move(Position start, Position end) {
        this.start = start;
        this.end = end;
    }

    @Override
    public String toString() {
        return "("+start.x+", "+start.y+") -> ("+end.x+", "+end.y+")";
    }

    public int dx() {
        return end.x - start.x;
    }

    public int dy() {
        return end.y - start.y;
    }

}

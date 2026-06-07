/**
 * Classe pour gérer les conversions de coordonnées en notation algébrique et inversement.
 */

package logic.utils;

import logic.game.Position;

public class AlgebraicNotation {

    /**
     * Conversion en notation algébrique
     * @param position Les coordonnées
     * @return Notation algébrique de ces coordonnées
     */
    public static String toAlgebraicNotation(Position position) {
        return "" + (char)(97 + position.y) + (8 - position.x);
    }

    /** Conversion en coordonnées
     * @param algebraicNotation Notation algébrique
     * @return Coordonnées
     */
    public static Position toCoordinates(String algebraicNotation) {
        int y = algebraicNotation.charAt(0) - 97;
        int x = 8 - Character.getNumericValue(algebraicNotation.charAt(1));

        return new Position(x, y);
    }

}
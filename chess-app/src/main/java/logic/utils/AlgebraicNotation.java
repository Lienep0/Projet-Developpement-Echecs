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
        return "" + (char)(65+position.x) + (7-position.y);
    }

    /** Conversion en coordonnées
     * @param algebraicNotation Notation algébrique (lettres en MAJUSCULES)
     * @return Coordonnées
     */
    public static Position toCoordinates(String algebraicNotation) {
        return new Position(algebraicNotation.charAt(0)-65, 7-Integer.parseInt(String.valueOf(algebraicNotation.charAt(1))));
    }

}

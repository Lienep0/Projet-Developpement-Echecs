/**
 * Classe permettant de définir les deux couleurs de pièces.
 */

package logic.game;

public enum Color {

    WHITE, BLACK;

    public Color opposite() {
        if (this == WHITE) {
            return BLACK;
        }
        return WHITE;
    }
}

/**
 * Classe permettant de représenter un plateau de jeu.
 */

package logic.game;

import logic.exceptions.OutOfBoardException;
import logic.pieces.*;
import static logic.game.Color.*;

public class Board {

    private Piece[][] array;
    private Move lastMove;

    public Board() {
        array = new Piece[8][8];

        // On place les pièces
        // Pions
        for (int i=0; i<8; i++) {
            array[1][i] = new Pawn(BLACK);
            array[6][i] = new Pawn(WHITE);
        }
        // Tours
        array[0][0] = new Rook(BLACK);
        array[0][7] = new Rook(BLACK);
        array[7][0] = new Rook(WHITE);
        array[7][7] = new Rook(WHITE);
        // Cavaliers
        array[0][1] = new Knight(BLACK);
        array[0][6] = new Knight(BLACK);
        array[7][1] = new Knight(WHITE);
        array[7][6] = new Knight(WHITE);
        // Fous
        array[0][2] = new Bishop(BLACK);
        array[0][5] = new Bishop(BLACK);
        array[7][2] = new Bishop(WHITE);
        array[7][5] = new Bishop(WHITE);
        // Reines
        array[0][3] = new Queen(BLACK);
        array[7][3] = new Queen(WHITE);
        // Rois
        array[0][4] = new King(BLACK);
        array[7][4] = new King(WHITE);
    }

    public Piece getPieceAt(int x, int y) throws OutOfBoardException {
        if (x<0 || x>7 || y<0 || y>7) {
            throw new OutOfBoardException("Les coordonnées dépassent du plateau.");
        }
        return array[x][y];
    }

    public Piece[][] getArray() {
        return array;
    }

    public Move getLastMove() {
        return lastMove;
    }

    public Move updateLastMove(Move lastMove) {
        this.lastMove = lastMove;
    }

    /**
     * Vérifie qu'un chemin entre deux points du plateau est libre : permet de valider
     * des déplacements de pièces comme le fou ou la tour.
     * @param move Déplacement entre deux points
     * @return true si le chemin est libre entre ces deux points (aucune pièce)
     */
    public boolean isPathClear(Move move) {

        int dx = move.dx();
        int dy = move.dy();

        // On ne peut vérifier que les mouvements horizontaux ou verticaux
        boolean isStraight = dx == 0 || dy == 0;
        boolean isDiagonal = Math.abs(dx) == Math.abs(dy);
        if (!isStraight && !isDiagonal) return false;

        int sx = Integer.compare(dx, 0); // step x (sx) = 1 si dx > 0, 0 si dx = 0, -1 si dx < 0
        int sy = Integer.compare(dy, 0);

        int i = move.start.x + sx;
        int j = move.start.y + sy;

        while (i != move.end.x || j != move.end.y) {
            if (getPieceAt(i, j) != null) return false;
            i += sx;
            j += sy;
        }

        return true;

    }

    /**
     * Vérifie si une case peut être attaquée ou non par l'adversaire
     * @param target Case concernée
     * @param color Couleur de la pièce menacée (opposé de l'attaquant)
     * @return true si la case peut en effet être attaquée
     */
    public boolean isAttacked(Position target, Color color) {
        for (int x=0; x<8; x++) {
            for (int y=0; y<8; y++) {
                Piece piece = getPieceAt(x, y);
                if (piece != null && piece.getColor() != color) {
                    Move move = new Move(new Position(x,y), target);
                    if (piece.canAttack(move, this)) return true;
                }
            }
        }
        return false;
    }

}

/**
 * Classe abstraite représentant une pièce de jeu.
 * Gère la couleur de la pièce et les bases des mouvements (les règles spécifiques à chaque pièce
 * sont implémentées dans les classes filles).
 */

package logic.pieces;

import logic.game.*;
import logic.exceptions.OutOfBoardException;
import java.util.ArrayList;
import java.util.List;

public abstract class Piece {

    protected Color color;
    protected boolean hasMoved;

    public Piece(Color color) {
        this.color = color;
        this.hasMoved = false;
    }

    public Color getColor() {
        return color;
    }

    public boolean getHasMoved() {
        return hasMoved;
    }

    public void makeMoved() { this.hasMoved = true; }

    public boolean isValidMove(Move move, Board board) throws OutOfBoardException {

        // Déplacement dans les limites du plateau
        if (move.start.x<0 || move.start.x>7 || move.start.y<0 || move.start.y>7
            || move.end.x<0 || move.end.x>7 || move.end.y<0 || move.end.y>7
        ) {
            throw new OutOfBoardException("Mouvement en dehors du plateau.");
        }

        // Il y a déplacement
        if (move.dx() == 0 && move.dy() == 0) return false;

        // Arrivée pas déjà occupée par la même couleur
        Piece target = board.getPieceAt(move.end.x, move.end.y);
        if (target != null && target.color == color) return false;

        // Mode de déplacement de la pièce respecté
        return isPieceMove(move, board);

    }

    protected abstract boolean isPieceMove(Move move, Board board);

    public abstract boolean canAttack(Move move, Board board);

    public List<Move> getValidMoves(Position position, Board board) {
        List<Move> validMoves = new ArrayList<Move>();
        for (int i=0; i<8; i++) {
            for (int j=0; j<8; j++) {
                Move move = new Move(position, new Position(i, j));
                if (isValidMove(move, board)) validMoves.add(move);
            }
        }
        return validMoves;
    }

}

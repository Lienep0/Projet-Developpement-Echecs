package logic.pieces;

import logic.game.*;

import static logic.game.Color.BLACK;
import static logic.game.Color.WHITE;

public class Pawn extends Piece {

    public Pawn(Color color) {
        super(color);
    }

    @Override
    public Piece copy() {
        return new Pawn(this.getColor());
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {

        int dx = move.dx();
        int dy = move.dy();
        int dir = (color == WHITE) ? -1 : 1;
        int startRow = (color == WHITE) ? 6 : 1;
        Piece target = board.getPieceAt(move.end);

        // Cas tout droit (avance le long de l'axe x / rangée)
        if (dy == 0) {
            if (target != null) return false; // Case d'arrivée vide
            if (dx == dir) return true; // Direction respectée

            // Cas où on avance de 2
            if (move.start.x == startRow && dx == 2 * dir) {
                Position mid = new Position(move.start.x + dir, move.start.y);
                return board.getPieceAt(mid) == null; // La case intermédiaire doit être vide
            }
        }

        // Cas diagonal
        if (Math.abs(dy) == 1 && dx == dir) {
            return target != null || isEnPassant(move, board); // Il faut une pièce à capturer (couleur vérifiée dans isValidMove dans Piece)
        }

        return false;

    }

    private boolean isEnPassant(Move move, Board board) {
        Move lastMove = board.getLastMove();
        if (lastMove != null && board.getPieceAt(lastMove.end) instanceof Pawn && Math.abs(lastMove.dx()) == 2) {
            if (
                    (color == WHITE && move.end.x == lastMove.end.x - 1 && move.end.y == lastMove.end.y)
                            || (color == BLACK && move.end.x == lastMove.end.x + 1 && move.end.y == lastMove.end.y)
            ) {
                return true;
            }
        }
        return false;
    }

    @Override
    public boolean canAttack(Move move, Board board) {
        int dir = (color == WHITE) ? -1 : 1;
        return (Math.abs(move.dy()) == 1 && move.dx() == dir);
    }

}

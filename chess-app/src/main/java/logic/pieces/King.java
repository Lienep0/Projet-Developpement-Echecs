package logic.pieces;

import logic.game.*;

import static logic.game.Color.WHITE;

public class King extends Piece {

    public King(Color color) {
        super(color);
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {
        if (isCastling(move, board)) return true;
        if (Math.abs(move.dx()) > 1 || Math.abs(move.dy()) > 1) return false;
        return true;
    }

    private boolean isCastling(Move move, Board board) {

        int dx = move.dx();
        int dy = move.dy();

        // Il faut que le roi n'ait pas bougé
        if (hasMoved) return false;

        // Roque : déplacement de deux à gauche ou deux à droite
        if ((dx != 2 && dx != -2) || dy != 0) return false;

        int y = (color == WHITE) ? 7 : 0;

        // Il faut que la tour n'ait pas bougé
        Piece rook = (dx == 2) ? board.getPieceAt(7, y) : board.getPieceAt(0, y);
        if (!(rook instanceof Rook) || rook.getHasMoved()) return false;

        // Le chemin doit être libre
        if (!board.isPathClear(move)) return false;

        // Le chemin ne doit pas être contrôlé par l'adversaire
        int x = move.start.x;
        int dir = (dx == 2) ? 1 : -1;
        for (int i=0; Math.abs(i)<3; i+=dir) {
            if (board.isAttacked(new Position(x+i, y), color)) return false;
        }

        return true;

    }

    public boolean canAttack(Move move, Board board) {
        return Math.abs(move.dx()) <= 1 && Math.abs(move.dy()) <= 1;
    }

}

package logic.pieces;

import logic.game.*;

public class Rook extends Piece {

    public Rook(Color color) {
        super(color);
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {

        // Déplacement horizontal ou vertical
        if (move.dx() != 0 && move.dy() != 0) return false;

        // Chemin vide
        return board.isPathClear(move);

    }

    @Override
    public boolean canAttack(Move move, Board board) {
        return isPieceMove(move, board);
    }

}

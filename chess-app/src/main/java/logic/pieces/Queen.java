package logic.pieces;

import logic.game.*;

public class Queen extends Piece {

    public Queen(Color color) {
        super(color);
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {

        // Déplacement diagonal ou horizontal
        if (move.dx() != 0 && move.dy() != 0 && Math.abs(move.dx()) != Math.abs(move.dy())) return false;

        // Chemin vide
        return board.isPathClear(move);

    }

    @Override
    public boolean canAttack(Move move, Board board) {
        return isPieceMove(move, board);
    }

}

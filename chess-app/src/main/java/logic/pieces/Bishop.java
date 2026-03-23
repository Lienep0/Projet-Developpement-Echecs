package logic.pieces;

import logic.game.*;

public class Bishop extends Piece {

    public Bishop(Color color) {
        super(color);
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {

        // Déplacement diagonal
        if (Math.abs(move.dx()) != Math.abs(move.dy())) return false;

        // Chemin vide
        return board.isPathClear(move);

    }

    @Override
    public boolean canAttack(Move move, Board board) {
        return isPieceMove(move, board);
    }

}

package logic.pieces;

import logic.game.*;

public class Knight extends Piece {

    public Knight(Color color) {
        super(color);
    }

    @Override
    protected boolean isPieceMove(Move move, Board board) {
        if (Math.abs(move.dx() * move.dy()) != 2) return false;
        return true;
    }

    @Override
    public boolean canAttack(Move move, Board board) {
        return isPieceMove(move, board);
    }

}

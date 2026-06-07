package logic.utils;

import logic.game.GameEngine;
import logic.game.Move;
import logic.game.Position;
import logic.pieces.*;
import static logic.game.Color.*;

public class FenConversion {

    public static String toFen(GameEngine game) {

        String result = "";
        Piece[][] board = game.getBoard();

        // Construction du plateau
        for (int i = 0; i < 8; i++) {
            int consecutiveEmptySquares = 0;
            for (int j = 0; j < 8; j++) {
                Piece piece = board[i][j];
                if (piece == null) {
                    consecutiveEmptySquares++;
                } else {
                    if (consecutiveEmptySquares > 0) {
                        result = result.concat(Integer.toString(consecutiveEmptySquares));
                        consecutiveEmptySquares = 0;
                    }
                    String pieceLetter = "";
                    if (piece instanceof Pawn)   pieceLetter = "p";
                    if (piece instanceof Knight) pieceLetter = "n";
                    if (piece instanceof Bishop) pieceLetter = "b";
                    if (piece instanceof Rook)   pieceLetter = "r";
                    if (piece instanceof Queen)  pieceLetter = "q";
                    if (piece instanceof King)   pieceLetter = "k";
                    if (piece.getColor() == WHITE) {
                        pieceLetter = pieceLetter.toUpperCase();
                    }
                    result = result.concat(pieceLetter);
                }
            }
            if (consecutiveEmptySquares > 0) {
                result = result.concat(Integer.toString(consecutiveEmptySquares));
            }
            if (i < 7) {
                result = result.concat("/");
            }
        }

        // Couleur du joueur
        if (game.getCurrentPlayer() == WHITE) {
            result = result.concat(" w ");
        } else {
            result = result.concat(" b ");
        }

        // Possibilités de roque
        boolean atLeastOneCastle = false;
        if (!board[7][4].getHasMoved()) { // Roi blanc
            if (!board[7][7].getHasMoved()) { // Tour blanche droite
                result = result.concat("K");
                atLeastOneCastle = true;
            }
            if (!board[7][0].getHasMoved()) { // Tour blanche gauche
                result = result.concat("Q");
                atLeastOneCastle = true;
            }
        }
        if (!board[0][4].getHasMoved()) { // Roi noir
            if (!board[0][7].getHasMoved()) { // Tour noire droite
                result = result.concat("k");
                atLeastOneCastle = true;
            }
            if (!board[0][0].getHasMoved()) { // Tour noire gauche
                result = result.concat("q");
                atLeastOneCastle = true;
            }
        }
        if (!atLeastOneCastle) {
            result = result.concat("-");
        }
        result = result.concat(" ");

        // En passant
        Move lastMove = game.getLastMove();
        if (lastMove == null) {
            result = result.concat("-");
        } else {
            Position finalPos = lastMove.end;
            Piece piece = board[finalPos.x][finalPos.y];
            if (
                    piece instanceof Pawn
                            &&
                            lastMove.dx() == 2
                            && (
                            (finalPos.x == 3 && game.getCurrentPlayer() == WHITE)
                                    ||
                                    (finalPos.x == 4 && game.getCurrentPlayer() == BLACK)
                    )
            ) {
                Position possibleEnPassant = new Position(finalPos.x - 1, finalPos.y);
                result = result.concat(AlgebraicNotation.toAlgebraicNotation(possibleEnPassant));
            } else {
                result = result.concat("-");
            }
        }
        result = result.concat(" ");

        // Flemme de compter les coups, à changer si ça marche pas
        result = result.concat("0 0");

        return result;
    }

}

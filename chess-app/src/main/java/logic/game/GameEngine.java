/**
 * Classe principale : moteur de jeu
 */

package logic.game;

import logic.pieces.Piece;

import static logic.game.Color.WHITE;

public class GameEngine {

    private Board board;
    private Color currentPlayer;

    public GameEngine() {
        board = new Board();
        currentPlayer = WHITE;
    }

    public Piece[][] getBoard() {
        return board.getArray();
    }

    public Color getCurrentPlayer() {
        return currentPlayer;
    }

    public MoveResult playMove(Move move) {
        return new MoveResult(true, new Board(), WHITE, WHITE);
    }

}

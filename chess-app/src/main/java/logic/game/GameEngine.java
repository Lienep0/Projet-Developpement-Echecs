/**
 * Classe principale : moteur de jeu
 */

package logic.game;

import java.util.ArrayList;
import java.util.List;

import logic.exceptions.OutOfBoardException;
import logic.pieces.*;

import static logic.game.Color.*;

public class GameEngine {

    // L'état d'une partie est réduit à l'état du plateau et au joueur qui doit jouer
    private Board board;
    private Color currentPlayer;

    public GameEngine() {
        board = new Board();
        currentPlayer = WHITE;
    }

    // Guetteurs
    public Piece[][] getBoard() {
        return board.getArray();
    }

    public Color getCurrentPlayer() {
        return currentPlayer;
    }

    public Move getLastMove() {
        return board.getLastMove();
    }

    /**
     * Méthode principale, permet de jouer un coup.
     * @param move Coup à jouer
     * @return moveResult qui indique si le coup a pu être joué, et l'état du jeu après ce coup
     */
    public MoveResult playMove(Move move) {

        // Vérifier que la case de départ n'est pas vide
        Piece piece = board.getPieceAt(move.start);
        if (piece == null) {
        	System.out.println("pas de pièce");
        	return new MoveResult(false, "noPiece", board, currentPlayer, null);
        }

        // Vérifier que c'est bien au tour de ce joueur
        Color currentPlayer = piece.getColor();
        Color opponent = currentPlayer.opposite();
        if (currentPlayer != this.currentPlayer) return new MoveResult(false, "notPlayerTurn", board, currentPlayer, null);

        // Vérifier que le coup est légal (au sens des capacités de la pièce)
        try {
            if (!piece.isValidMove(move, board)) {
            	
            	System.out.println("coup invalide");
            	return new MoveResult(false, "invalidMove", board, currentPlayer, null);
            }
        } catch (OutOfBoardException e) {
        	System.out.println("out of board");
            return new MoveResult(false, "outOfBoard", board, currentPlayer, null);
        }

        // On joue temporairement le coup sur le plateau pour effectuer les vérifications suivantes
        Board newBoard = new Board(board);
        newBoard.executeMove(move);
        

        // Vérifier si le coup permet une promotion (auquel cas on promeut immédiatement à une Reine pour l'instant)
        if (piece instanceof Pawn) {
            int promotionRow = (currentPlayer == WHITE) ? 0 : 7;
            if (move.end.x == promotionRow) {
                Piece queen = new Queen(currentPlayer);
                queen.makeMoved();
                newBoard.updateArray(move.end, queen);
            }
        }

        // Vérifier si le coup est un roque (et déplacer la tour associée si c'est le cas)
        if (piece instanceof King && Math.abs(move.dy()) == 2) {
            int row = move.start.x;
            if (move.end.y == 6) { // Petit roque
                Piece rook = newBoard.getPieceAt(new Position(row, 7));
                rook.makeMoved();
                newBoard.updateArray(new Position(row, 5), rook);
                newBoard.updateArray(new Position(row, 7), null);
      
            }
            else if (move.end.y == 2) { // Grand roque
                Piece rook = newBoard.getPieceAt(new Position(row, 0));
                rook.makeMoved();
                newBoard.updateArray(new Position(row, 3), rook);
                newBoard.updateArray(new Position(row, 0), null);
               
                
            }
        }

        // Vérifier que le coup ne met pas le joueur en échec
        if (currentPlayer == WHITE) {
            if (newBoard.isAttacked(newBoard.getWhiteKingPos(), WHITE)) {
            	System.out.println("le roi blanc est attaqué");
            	return new MoveResult(false, "putPlayerInCheck", board, currentPlayer, null);
            }
        } else {
            if (newBoard.isAttacked(newBoard.getBlackKingPos(), BLACK)) {
            	System.out.println("le roi noir est attaqué");
            	return new MoveResult(false, "putPlayerInCheck", board, currentPlayer, null);
            }
        }
        this.board = newBoard;
        this.currentPlayer = opponent;
        // Vérifier si le coup aboutit à une position finale
        boolean opponentCanMove = hasPossibleMoves(opponent, newBoard);
        boolean opponentInCheck = newBoard.isAttacked(
                (opponent == WHITE) ? newBoard.getWhiteKingPos() : newBoard.getBlackKingPos(),
                opponent
        );
        
        if (!opponentCanMove) {
            if (opponentInCheck) {
            	System.out.println("checkmate");
                return new MoveResult(true, "checkmate", newBoard, opponent, currentPlayer);
            } else {
            	System.out.println("stalemate");
                return new MoveResult(true, "stalemate", newBoard, opponent, currentPlayer);
            }
        }
        if (opponentInCheck) {
        	System.out.println("check");
        	this.board = newBoard;
            this.currentPlayer = opponent;
            return new MoveResult(true, "check", newBoard, opponent, null);
        }

        // Sinon, valider le coup et renvoyer l'état actuel du jeu
        
        
        
        return new MoveResult(true, "", newBoard, opponent, null);
        
    }

    /**
     * Renvoie une liste de coups possibles pour une pièce.
     * @param position position de départ
     * @return liste de coups possibles
     */
    public List<Move> getPossibleMoves(Position position) {

        Piece piece = board.getPieceAt(position);
        if (piece == null) return new ArrayList<>();

        List<Move> potentialPossibleMoves = piece.getValidMoves(position, board);
        List<Move> possibleMoves = new ArrayList<>();

        // Filtrage (on ne garde pas les coups qui nous mettent en Échec)
        for (Move move : potentialPossibleMoves) {

            Board newBoard = new Board(board);
            newBoard.executeMove(move);

            Position kingPos = (piece.getColor() == WHITE)
                    ? newBoard.getWhiteKingPos()
                    : newBoard.getBlackKingPos();

            if (!newBoard.isAttacked(kingPos, piece.getColor())) {
                possibleMoves.add(move);
            }
        }

        return possibleMoves;
    }

    /**
     * Vérifie si un joueur peut au moins jouer un coup (utile pour Pat ou Mat).
     * @param player joueur concerné
     * @param board plateau
     * @return true si le joueur peut jouer un coup
     */
    public boolean hasPossibleMoves(Color player, Board board) {

        for (int i=0; i<8; i++) {
            for (int j=0; j<8; j++) {

                Position position = new Position(i, j);
                Piece piece = board.getPieceAt(position);

                if (piece != null && piece.getColor() == player) {
                    if (!getPossibleMoves(position).isEmpty()) {
                    	
                        return true;
                    }
                    
                }

            }
        }

        return false;

    }

}

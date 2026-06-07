/**
 * Classe permettant de représenter un plateau de jeu.
 */

package logic.game;

import logic.exceptions.OutOfBoardException;
import logic.pieces.*;
import static logic.game.Color.*;

public class Board {

    // On stocke l'état du plateau et le dernier coup joué
    private Piece[][] array;
    private Move lastMove;
    // On stocke aussi la position des rois, car on a souvent besoin d'y avoir accès
    // (cela nous évite une recherche inutile)
    private Position whiteKingPos;
    private Position blackKingPos;

    public Board() {
        array = new Piece[8][8];
        lastMove = null;
        whiteKingPos = new Position(7, 4);
        blackKingPos = new Position(0, 4);

        // On place les pièces
        // Pions
        for (int i=0; i<8; i++) {
            array[1][i] = new Pawn(BLACK);
            array[6][i] = new Pawn(WHITE);
        }
        // Tours
        array[0][0] = new Rook(BLACK);
        array[0][7] = new Rook(BLACK);
        array[7][0] = new Rook(WHITE);
        array[7][7] = new Rook(WHITE);
        // Cavaliers
        array[0][1] = new Knight(BLACK);
        array[0][6] = new Knight(BLACK);
        array[7][1] = new Knight(WHITE);
        array[7][6] = new Knight(WHITE);
        // Fous
        array[0][2] = new Bishop(BLACK);
        array[0][5] = new Bishop(BLACK);
        array[7][2] = new Bishop(WHITE);
        array[7][5] = new Bishop(WHITE);
        // Reines
        array[0][3] = new Queen(BLACK);
        array[7][3] = new Queen(WHITE);
        // Rois
        array[0][4] = new King(BLACK);
        array[7][4] = new King(WHITE);
    }

    /**
     * Constructeur permettant de faire une copie d'un plateau (utile pour les simulations)
     * @param old plateau à copier
     */
    public Board(Board old) {

        this.array = new Piece[8][8];

        for (int x = 0; x < 8; x++) {
            for (int y = 0; y < 8; y++) {
                Piece p = old.array[x][y];
                if (p != null) {
                    this.array[x][y] = p.copy(); // On a implémenté une méthode pour copier les pièces
                } else {
                    this.array[x][y] = null;
                }
            }
        }

        this.whiteKingPos = new Position(old.whiteKingPos.x, old.whiteKingPos.y);
        this.blackKingPos = new Position(old.blackKingPos.x, old.blackKingPos.y);

        if (old.lastMove != null) {
            this.lastMove = new Move(
                    new Position(old.lastMove.start.x, old.lastMove.start.y),
                    new Position(old.lastMove.end.x, old.lastMove.end.y)
            );
        } else {
            this.lastMove = null;
        }

    }

    // Guetteurs
    public Piece getPieceAt(Position position) throws OutOfBoardException {
        int x = position.x;
        int y = position.y;
        if (x<0 || x>7 || y<0 || y>7) {
            throw new OutOfBoardException("Les coordonnées dépassent du plateau.");
        }
        return array[x][y];
    }

    public Piece[][] getArray() {
        return array;
    }

    public Move getLastMove() {
        return lastMove;
    }

    public Position getWhiteKingPos() {
        return whiteKingPos;
    }

    public Position getBlackKingPos() {
        return blackKingPos;
    }

    // Setteurs
    public void updateArray(Position position, Piece piece) {
        array[position.x][position.y] = piece;
    }

    public void updateLastMove(Move lastMove) {
        this.lastMove = lastMove;
    }

    public void updateBlackKingPos(Position position) {
        blackKingPos = position;
    }

    public void updateWhiteKingPos(Position position) {
        whiteKingPos = position;
    }

    /**
     * Réalise un coup sur le plateau
     * @param move coup à réaliser
     */
    public void executeMove(Move move) {

        Piece piece = getPieceAt(move.start);
        piece.makeMoved();
        
        if (piece instanceof Pawn) {
        	if (move.start.y!=move.end.y) {
        		int dx = move.start.x -move.end.x;
        		
        		Piece pieceEnd = getPieceAt(move.end);
        		
        		
        		if (pieceEnd==null){
        			System.out.print("test");
        		
	        		
	        		updateArray(new Position(move.end.x + dx ,move.end.y), null);
	        		
        		
        		}
        		
        	}
        }
        updateArray(move.end, piece);

        if (piece instanceof King) {
            if (piece.getColor() == WHITE) {
                updateWhiteKingPos(move.end);
            } else {
                updateBlackKingPos(move.end);
            }
        }
        
        updateLastMove(move);

        updateArray(move.start, null);

    }

    /**
     * Vérifie qu'un chemin entre deux points du plateau est libre : permet de valider
     * des déplacements de pièces comme le fou ou la tour.
     * @param move Déplacement entre deux points
     * @return true si le chemin est libre (strictement) entre ces deux points (aucune pièce)
     */
    public boolean isPathClear(Move move) {

        int dx = move.dx();
        int dy = move.dy();

        // On ne peut vérifier que les mouvements horizontaux ou verticaux
        boolean isStraight = dx == 0 || dy == 0;
        boolean isDiagonal = Math.abs(dx) == Math.abs(dy);
        if (!isStraight && !isDiagonal) return false;

        int sx = Integer.compare(dx, 0); // step x (sx) = 1 si dx > 0, 0 si dx = 0, -1 si dx < 0
        int sy = Integer.compare(dy, 0);

        int i = move.start.x + sx;
        int j = move.start.y + sy;

        while (i != move.end.x || j != move.end.y) {
            if (getPieceAt(new Position(i, j)) != null) return false;
            i += sx;
            j += sy;
        }

        return true;

    }

    /**
     * Vérifie si une case peut être attaquée ou non par l'adversaire
     * @param target Case concernée
     * @param color Couleur de la pièce menacée (opposé de l'attaquant)
     * @return true si la case peut en effet être attaquée
     */
    public boolean isAttacked(Position target, Color color) {
        for (int x=0; x<8; x++) {
            for (int y=0; y<8; y++) {
                Piece piece = getPieceAt(new Position(x, y));
                if (piece != null && piece.getColor() != color) {
                    Move move = new Move(new Position(x,y), target);
                    if (piece.canAttack(move, this)) return true;
                }
            }
        }
        return false;
    }

}

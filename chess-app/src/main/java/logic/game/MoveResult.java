/**
 * Classe permettant de stocker les résultats d'une action d'un joueur
 * (coup possible ou non, plateau, joueur suivant, fin de partie).
 */

package logic.game;

public class MoveResult {

    public final boolean success;
    public  final Board board;
    public final Color currentPlayer;
    public final Color winner; // null si le jeu n'est pas fini

    public MoveResult(boolean success,
               Board board,
               Color currentPlayer,
               Color winner
    ) {
        this.success = success;
        this.board = board;
        this.currentPlayer = currentPlayer;
        this.winner = winner;
    }

}

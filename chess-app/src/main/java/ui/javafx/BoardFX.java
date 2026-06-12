package ui.javafx;

import javafx.geometry.Rectangle2D;
import javafx.stage.Screen;
import logic.game.Color;
import logic.pieces.Bishop;
import logic.pieces.King;
import logic.pieces.Knight;
import logic.pieces.Pawn;
import logic.pieces.Piece;
import logic.pieces.Queen;
import logic.pieces.Rook;

public class BoardFX {

    private Sprite[][] spriteArray;
    public Sprite selectedSprite;
    String typeMatch;
    
    
    //prend la taille de l'écran
    static Rectangle2D bounds = Screen.getPrimary().getBounds();
	static int L = (int) bounds.getHeight();
	static int l = L/10;
	//initialise un boardfx
    public BoardFX() {
        spriteArray = new Sprite[8][8];
        selectedSprite =null;
        
        
    }

    public Sprite getSpriteAt(int x, int y) {
        return spriteArray[x][y];
    }

    public Sprite[][] getArray() {
        return spriteArray;
    }
    //met à jour l'echequier apres un coup à partir de l'echequier du moteur de jeu
    public void updateMove(Piece[][] board) {
    	int a=1;
    	int b=1;
    	for (int i=0; i<8; i++) {
    		for (int j=0; j<8; j++) {
    			a=i+1;	
    			b=j+1;
    			Piece piece = board[j][i];
    			if (piece!=null) {
	    			if (piece.getColor()== Color.BLACK) {
	    				if (piece instanceof Bishop) {spriteArray[i][j]=new Sprite("fou_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof King) {spriteArray[i][j]=new Sprite("roi_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Knight) {spriteArray[i][j]=new Sprite("cheval_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Pawn) {spriteArray[i][j]=new Sprite("pion_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Queen) {spriteArray[i][j]=new Sprite("reine_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Rook) {spriteArray[i][j]=new Sprite("tour_noir.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				
	    			} else {
	    				if (piece instanceof Bishop) {spriteArray[i][j]=new Sprite("fou.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof King) {spriteArray[i][j]=new Sprite("roi.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Knight) {spriteArray[i][j]=new Sprite("cheval.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Pawn) {spriteArray[i][j]=new Sprite("pion.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Queen) {spriteArray[i][j]=new Sprite("reine.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				if (piece instanceof Rook) {spriteArray[i][j]=new Sprite("tour.png",l);
	    				spriteArray[i][j].setPosition(a*l, b*l);}
	    				
	    			}
    			}else {
    				spriteArray[i][j]=null;
    			}
    			
    		}
    	}
    }
    
    
}
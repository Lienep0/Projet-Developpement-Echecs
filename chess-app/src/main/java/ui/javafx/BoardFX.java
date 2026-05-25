package ui.javafx;

import javafx.scene.canvas.GraphicsContext;
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
    
    
    
    int l=32;

    public BoardFX() {
        spriteArray = new Sprite[8][8];
        selectedSprite =null;
        /*
        for (int i=0; i<8; i++) {
        	spriteArray[i][1]=new Sprite("pion_noir.png",l);
        	spriteArray[i][1].setPosition((i+1)*l,2*l);
        	spriteArray[i][6]=new Sprite("pion.png",l);
        	spriteArray[i][6].setPosition((i+1)*l,7*l);
        }
        spriteArray[0][0]=new Sprite("tour_noir.png",l);
    	spriteArray[0][0].setPosition(1*l,1*l);
    	spriteArray[7][0]=new Sprite("tour_noir.png",l);
    	spriteArray[7][0].setPosition(8*l,1*l);
    	spriteArray[0][7]=new Sprite("tour.png",l);
    	spriteArray[0][7].setPosition(1*l,8*l);
    	spriteArray[7][7]=new Sprite("tour.png",l);
    	spriteArray[7][7].setPosition(8*l,8*l);
    	
    	spriteArray[1][0]=new Sprite("cheval_noir.png",l);
    	spriteArray[1][0].setPosition(2*l,1*l);
    	spriteArray[6][0]=new Sprite("cheval_noir.png",l);
    	spriteArray[6][0].setPosition(7*l,1*l);
    	spriteArray[1][7]=new Sprite("cheval.png",l);
    	spriteArray[1][7].setPosition(2*l,8*l);
    	spriteArray[6][7]=new Sprite("cheval.png",l);
    	spriteArray[6][7].setPosition(7*l,8*l);
    	
    	spriteArray[2][0]=new Sprite("fou_noir.png",l);
    	spriteArray[2][0].setPosition(3*l,1*l);
    	spriteArray[5][0]=new Sprite("fou_noir.png",l);
    	spriteArray[5][0].setPosition(6*l,1*l);
    	spriteArray[2][7]=new Sprite("fou.png",l);
    	spriteArray[2][7].setPosition(3*l,8*l);
    	spriteArray[5][7]=new Sprite("fou.png",l);
    	spriteArray[5][7].setPosition(6*l,8*l);
    	
    	spriteArray[3][0]=new Sprite("reine_noir.png",l);
    	spriteArray[3][0].setPosition(4*l,1*l);
    	spriteArray[3][7]=new Sprite("reine.png",l);
    	spriteArray[3][7].setPosition(4*l,8*l);
    	
    	spriteArray[4][0]=new Sprite("roi_noir.png",l);
    	spriteArray[4][0].setPosition(5*l,1*l);
    	spriteArray[4][7]=new Sprite("roi.png",l);
    	spriteArray[4][7].setPosition(5*l,8*l); */
        
        
        
        
        
        
    }

    public Sprite getSpriteAt(int x, int y) {
        return spriteArray[x][y];
    }

    public Sprite[][] getArray() {
        return spriteArray;
    }
    
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
    
    public void update() {
    	for (int i=0;i<spriteArray.length;i++) {
    		for (int j=0;j<spriteArray.length;j++) {
    			spriteArray[i][j].setPosition((i+1)*l,(j+1)*l);
        		
        	}
    	}
    }
}
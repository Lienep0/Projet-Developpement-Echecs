package ui.javafx;



public class BoardFX {

    private Sprite[][] spriteArray;
    public Sprite selectedSprite;
    String typeMatch;
    
    
    
    int l=32;

    public BoardFX() {
        spriteArray = new Sprite[8][8];
        selectedSprite =null;
        Sprite pion1 = new Sprite("pion.png",l);
        spriteArray[0][0] = pion1;
        pion1.setPosition(l, l);
        Sprite pion2 = new Sprite("pion.png",l);
        spriteArray[0][1] = pion2;
        pion2.setPosition(l, 2*l);
    }

    public Sprite getSpriteAt(int x, int y) {
        return spriteArray[x][y];
    }

    public Sprite[][] getArray() {
        return spriteArray;
    }
    public void update() {
    	for (int i=0;i<spriteArray.length;i++) {
    		for (int j=0;j<spriteArray.length;j++) {
    			spriteArray[i][j].setPosition((i+1)*l,(j+1)*l);
        		
        	}
    	}
    }
}
package ui.javafx;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import logic.game.Position;

public class Sprite {
	Image image;
	int l;
	Position p;
	//initialise un sprite avec le nom du png et sa taille
	Sprite(String name, int l) {
		this.image = new Image(name,l,l,false,false);
		this.l=l;
		this.p=new Position(0,0);
	}
	void setPosition(int x, int y) {
		this.p = new Position(x,y);
	}

	//affichage au tour des noirs (plateau inversé)
	void renderBlack(GraphicsContext gc) {
		gc.drawImage(this.image, this.p.x,9*l-this.p.y);
	}
	//affichage au tour des blancs
	void render(GraphicsContext gc) {
		gc.drawImage(this.image, this.p.x,this.p.y);
		
	}
}
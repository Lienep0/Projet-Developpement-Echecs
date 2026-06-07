package ui.javafx;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import logic.game.Position;

public class Sprite {
	Image image;
	int l;
	Position p;
	
	Sprite(String name, int l) {
		this.image = new Image(name,l,l,false,false);
		this.l=l;
		this.p=new Position(0,0);
	}
	void setPosition(int x, int y) {
		this.p = new Position(x,y);
	}

	
	void renderBlack(GraphicsContext gc) {
		gc.drawImage(this.image, this.p.x,9*l-this.p.y);
	}
	void render(GraphicsContext gc) {
		gc.drawImage(this.image, this.p.x,this.p.y);
		
	}
}
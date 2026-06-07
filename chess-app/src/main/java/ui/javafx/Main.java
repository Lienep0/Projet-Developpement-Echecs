package ui.javafx;
	


import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.stage.Screen;
import javafx.stage.Stage;
import logic.game.Board;
import logic.game.Color;
import logic.game.GameEngine;
import logic.game.Move;
import logic.game.MoveResult;
import logic.game.Position;
import logic.pieces.Piece;
import javafx.scene.Group;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.image.Image;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.text.Text;


public class Main extends Application {
	static Rectangle2D bounds = Screen.getPrimary().getBounds();
	static int L = (int) bounds.getHeight();
	static int l = L/10;
	GameEngine gameEngine = new GameEngine();
	List<Move> moves = new ArrayList<>();
	@Override
	
	public void start(Stage stage) {

		
		
		TextField textField = new TextField();
        textField.setPromptText("Classic/Bot1/Bot2");


        Button button = new Button("Valider");
        button.setOnAction(e -> {
            String text = textField.getText();
            System.out.println("Texte saisi : " + text);

            
            stage.close();
            game(text);
        });
	
    
        VBox box = new VBox(10, textField, button);


        box.setStyle("-fx-padding: 20; -fx-alignment: center;");

        Scene scene1 = new Scene(box, 800, 400);
        stage.setScene(scene1);
        stage.setTitle("choisir le mode de jeu");
        stage.show();
        

		

        
		
	}
	private void game(String text) {
		BoardFX boardfx = new BoardFX();
		boardfx.updateMove(gameEngine.getBoard());
		
		boardfx.typeMatch=text;
		Stage stage = new Stage();
		Group root = new Group();
		Scene scene = new Scene(root);
		stage.setTitle("ChessApp");
		Image icon = new Image("pion.png");
		stage.getIcons().add(icon);
		
		
		
		stage.setResizable(true);
		stage.setFullScreen(true);
		Canvas canvas = new Canvas(L,L);
		Image fond = new Image("echequier.png",L,L,false,false);
		Image fondNoir = new Image("echequierNoir.png",L,L,false,false);
		Image vert = new Image("vert.png",l,l,false,false);
		Image rouge = new Image("rouge.png",l,l,false,false);
		Image white = new Image("white.png",2*l,l,false,false);
		Image black = new Image("black.png",2*l,l,false,false);
		
		
		root.getChildren().add(canvas);
		GraphicsContext gc = canvas.getGraphicsContext2D();

		
		
		
		stage.setScene(scene);
		stage.show();
		
		moves = new ArrayList<>();
		canvas.setOnMouseClicked(e -> {
			double x = e.getSceneX();
			double y = e.getSceneY();
			Position p = doubleToPosition(x,y);
			if (gameEngine.getCurrentPlayer()==Color.BLACK) {
				p=new Position(p.x,9*l-p.y);
			}
			
			Sprite next = boardfx.getSpriteAt((p.x)/l -1,(p.y)/l -1);
			
			Sprite cur = boardfx.selectedSprite;
			
			if (cur==null) {
				if (next!=null) {
					boardfx.selectedSprite=next;
					Piece[][] board = gameEngine.getBoard();
					if (board[(next.p.y)/l -1][(next.p.x)/l -1].getColor()==gameEngine.getCurrentPlayer()) {
						moves = gameEngine.getPossibleMoves(new Position((next.p.y)/l -1,(next.p.x)/l -1));
						gc.drawImage(vert, 0, 0);
					}
					
					
					
					
				}
			} else {
				Move move = new Move(new Position((cur.p.y)/l -1,(cur.p.x)/l -1),new Position((p.y)/l -1,(p.x)/l -1));
				MoveResult moveResult = gameEngine.playMove(move);

				if (moveResult.success==true) {
					
					boardfx.updateMove(gameEngine.getBoard());
					boardfx.selectedSprite=null;
					moves = new ArrayList<>();
					if (gameEngine.getCurrentPlayer()==Color.WHITE) {
						gc.drawImage(white, l, -5);						
					} else {
						gc.drawImage(black, l, -5);
					}
					gc.drawImage(rouge, 0, 0);
					
				}else {
					boardfx.selectedSprite=null;
					if (gameEngine.getCurrentPlayer()==Color.WHITE) {
						gc.drawImage(white, l, -5);						
					} else {
						gc.drawImage(black, l, -5);
					}
					gc.drawImage(rouge, 0, 0);
					
				}
			
			}
			
		});
		

		
		AnimationTimer at = new AnimationTimer() {
			@Override
			public void handle(long lo) {
				if (gameEngine.getCurrentPlayer()==Color.BLACK) {
					gc.drawImage(fond, 0, 0);
				} else {
					gc.drawImage(fondNoir, 0, 0);
				}
				for (int i=0;i<8;i++) {
		    		for (int j=0;j<8;j++) {
		    			if (boardfx.getArray()[i][j]!=null) {
		    				
		    				Sprite sprite= boardfx.getArray()[i][j];
		    				if (gameEngine.getCurrentPlayer()==Color.BLACK) {
		    					sprite.renderBlack(gc);
		    				} else {
		    					sprite.render(gc);
		    				}
		    				
		    				
		    			}
		        		
		        	}
		    	}
				Iterator<Move> it = moves.iterator();

				while (it.hasNext()) {
				    Move move = it.next();
				    Position pos = move.end;
				    int posx = pos.x;
				    int posy = pos.y;
				    Sprite violet = new Sprite("prev.png",l);
				    violet.setPosition((posy+1)*l, (posx+1)*l);
				    if (gameEngine.getCurrentPlayer()==Color.BLACK) {
    					violet.renderBlack(gc);
    				} else {
    					violet.render(gc);
    				}
				}


				
				
			}
		};
		at.start();
	}
	
	public static Position doubleToPosition(double x, double y) {
		return new Position((int)(x/l)*l,(int)(y/l)*l);
	}
	public static void main(String[] args) {
		
		launch(args);
	}
}

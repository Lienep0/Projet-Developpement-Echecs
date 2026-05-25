package ui.javafx;
	


import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
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


public class Main extends Application {
	int L = 320;
	static int l = 32;
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

        Scene scene1 = new Scene(box, 400, 200);
        stage.setScene(scene1);
        stage.setTitle("choisir le mode de jeu");
        stage.show();
		
	}
	private void game(String text) {
		Stage stage = new Stage();
		Group root = new Group();
		Scene scene = new Scene(root);
		stage.setTitle("ChessApp");
		Image icon = new Image("pion.png");
		stage.getIcons().add(icon);
		
		BoardFX board = new BoardFX();
		board.typeMatch=text;
		
		stage.setResizable(true);
		stage.setFullScreen(false);
		Canvas canvas = new Canvas(L,L);
		Image fond = new Image("echequier.png",L,L,false,false);
		Image vert = new Image("vert.png",l,l,false,false);
		Image rouge = new Image("rouge.png",l,l,false,false);
		root.getChildren().add(canvas);
		GraphicsContext gc = canvas.getGraphicsContext2D();

		
		
		
		stage.setScene(scene);
		stage.show();
		
		

		canvas.setOnMouseClicked(e -> {
			double x = e.getSceneX();
			double y = e.getSceneY();
			Position p = doubleToPosition(x,y);
			
			Sprite next = board.getSpriteAt((p.x)/l -1,(p.y)/l -1);
			
			Sprite cur = board.selectedSprite;
			
			if (cur==null) {
				if (next!=null) {
					board.selectedSprite=next;
					gc.drawImage(vert, 0, 0);
				}
			} else {
				if (next==null) {
					board.getArray()[(cur.p.x/l) -1][(cur.p.y)/l -1]=null;
					cur.setPosition(p.x,p.y);
					board.getArray()[(p.x/l) -1][(p.y)/l -1]=cur;
					cur.render(gc);
					board.selectedSprite=null;
					gc.drawImage(rouge, 0, 0);
					
				}else {
					board.selectedSprite=null;
					gc.drawImage(rouge, 0, 0);
					
				}
				
			}
			
		});
		

		
		AnimationTimer at = new AnimationTimer() {
			@Override
			public void handle(long lo) {
				gc.drawImage(fond, 0, 0);
				for (int i=0;i<board.getArray().length;i++) {
		    		for (int j=0;j<board.getArray().length;j++) {
		    			if (board.getArray()[i][j]!=null) {
		    				board.getArray()[i][j].render(gc);
		    			}
		        		
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

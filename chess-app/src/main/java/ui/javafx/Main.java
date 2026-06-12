package ui.javafx;
	




import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.geometry.Rectangle2D;
import javafx.stage.Screen;
import javafx.stage.Stage;
import logic.game.Color;
import logic.game.GameEngine;
import logic.game.Move;
import logic.game.MoveResult;
import logic.game.Position;
import logic.pieces.Pawn;
import logic.pieces.Piece;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.Button;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.layout.VBox;
import logic.utils.BotConnect;


public class Main extends Application {
	//prend la taille de l'écran
	static Rectangle2D bounds = Screen.getPrimary().getBounds();
	static int L = (int) bounds.getHeight();
	static int l = L/10;
	GameEngine gameEngine = new GameEngine();
	List<Move> moves = new ArrayList<>();
	List<Sprite> listeMangeeBlanc = new ArrayList<>();
	List<Sprite> listeMangeeNoir = new ArrayList<>();
	int time = 10;
	
	
	@Override
	//écran de sélection du mode de jeu
	public void start(Stage stage) {
		stage.setFullScreen(true);
		
		//box de choix du mode de jeu
		
        ChoiceBox<String> choiceBox = new ChoiceBox<>();
        choiceBox.getItems().addAll("classic","bot_algorithme","bot_reseau_de_neurones");
        choiceBox.setValue("classic");
        choiceBox.setStyle("-fx-font-size: 50px;");

        Button button = new Button("Valider");
        button.setStyle("-fx-font-size: 30px;");
        button.setOnAction(e -> {
            String text = choiceBox.getValue();

            if (text=="bot_algorithme") {
            	stage.close();
            	dropdown(stage,text);
            	
            }else {
            	stage.close();
                game(text);
            }
           
        }); 
	
        Label label = new Label("Choix du mode de jeu");
        label.setStyle("-fx-font-size: 32px;");
        VBox box = new VBox(10, label,choiceBox, button);


        box.setStyle("-fx-padding: 20; -fx-alignment: center;");

        Scene scene1 = new Scene(box, 800, 400);
        stage.setScene(scene1);
        stage.setTitle("choisir le mode de jeu");
        stage.show();
        

		

        
		
	}
	//écran de sélection du temps de jeu du bot algorithmique
	public void dropdown(Stage stage,String text) {
		stage.setFullScreen(true);
		
		//box de choix du mode de jeu
		
        ChoiceBox<String> choiceBox2 = new ChoiceBox<>();
        choiceBox2.getItems().addAll("5","10","20");
        choiceBox2.setValue("10");
        choiceBox2.setStyle("-fx-font-size: 50px;");

        Button button = new Button("Valider");
        button.setStyle("-fx-font-size: 30px;");
        button.setOnAction(e -> {
            time = Integer.valueOf(choiceBox2.getValue());

           
            stage.close();
            game(text);
        }); 
	
        Label label = new Label("Choix du temps de jeu du bot (en secondes)");
        label.setStyle("-fx-font-size: 32px;");
        VBox box = new VBox(10,label, choiceBox2, button);


        box.setStyle("-fx-padding: 20; -fx-alignment: center;");

        Scene scene1 = new Scene(box, 800, 400);
        stage.setScene(scene1);
        stage.setTitle("choisir le temps de jeu du bot");
        stage.show();
        

		

        
		
	}
	//début de la partie dans le mode de jeu "text"
	private void game(String text) {
		
		System.out.println("Dossier de travail actuel : " + System.getProperty("user.dir"));
		
		//setup de toutes les variables et images
		
		BoardFX boardfx = new BoardFX();
		boardfx.typeMatch=text;
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
		Canvas canvas = new Canvas(L*2,L);
		Image fondNoir = new Image("echequier.png",L,L,false,false);
		Image fond = new Image("echequierNoir.png",L,L,false,false);
		Image vert = new Image("vert.png",l,l,false,false);
		Image rouge = new Image("rouge.png",l,l,false,false);
		Image white = new Image("white.png",2*l,l,false,false);
		Image black = new Image("black.png",2*l,l,false,false);
		Image winW = new Image("winW.png",7*l,4*l,false,false);
		Image winB = new Image("winB.png",7*l,4*l,false,false);
		Image egalite = new Image("égalité.png",7*l,4*l,false,false);
		Image blanc = new Image("blanc.png",7*l,l,false,false);
		
		
		
		
		root.getChildren().add(canvas);
		GraphicsContext gc = canvas.getGraphicsContext2D();

		
		//bouton menu
		
		Button button = new Button("Menu");
		button.setPrefWidth(l*2);
		button.setPrefHeight(l);
		button.setLayoutX(13*l);
		button.setLayoutY(8*l);
		button.setStyle("-fx-font-size: 40px;");
        button.setOnAction(e -> {
            gameEngine = new GameEngine();
        	moves = new ArrayList<>();

            
            stage.close();
            start(stage);
        }); 
		
		root.getChildren().add(button);
		stage.setScene(scene);
		stage.show();
		
		//réinitialisation de la partie
		
		moves = new ArrayList<>();
		listeMangeeNoir = new ArrayList<>();
		listeMangeeBlanc = new ArrayList<>();
		
		//détection de clic sur l'écran
		
		canvas.setOnMouseClicked(e -> {
			double x = e.getSceneX();
			double y = e.getSceneY();
			Position p = doubleToPosition(x,y);
			if ((gameEngine.getCurrentPlayer()==Color.BLACK) && (boardfx.typeMatch=="classic")){
				p=new Position(p.x,9*l-p.y);
			}
			
			Sprite next = boardfx.getSpriteAt((p.x)/l -1,(p.y)/l -1);
			
			Sprite cur = boardfx.selectedSprite;
			
			//selection la piece si aucune n'est selection sinon joue le coup à partir de la piece pre-selectionnée
			
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
					PieceMangee(gc,next,move,boardfx);
					boardfx.updateMove(gameEngine.getBoard());
					boardfx.selectedSprite=null;
					moves = new ArrayList<>();
					gc.drawImage(rouge, 0, 0);
					
					

					if (moveResult.winner == Color.WHITE) {
						gc.drawImage(winW, 9*l, 2*l);
					}else { if (moveResult.winner == Color.BLACK) {
						gc.drawImage(winB, 9*l, 2*l);
						}
					}
					if (moveResult.errorCode=="stalemate") {
						gc.drawImage(egalite, 9*l, 2*l);
					}
					
					//si le mode de jeu est contre un bot -> laisse le bot jouer
					switch (boardfx.typeMatch) {
						

						case "bot_algorithme":
							String bot1Path = "../bot-echecs/main.py";

							// thread en arrière-plan pour ne pas bloquer la fenêtre JavaFX
							new Thread(() -> {
                                Move moveBot = null;
                                try {
                                    moveBot = BotConnect.askBot(bot1Path, gameEngine,time);
                                } catch (IOException ex) {
                                    throw new RuntimeException(ex);
                                }
								Move finalMoveBot = moveBot;
								javafx.application.Platform.runLater(() -> {
									if (finalMoveBot != null) {
										gameEngine.playMove(finalMoveBot);
										PieceMangee(gc,boardfx.getSpriteAt(finalMoveBot.end.y,finalMoveBot.end.x),finalMoveBot,boardfx);
										boardfx.updateMove(gameEngine.getBoard());
									}
								});
							}).start();
							break;

						case "bot_reseau_de_neurones":
							String bot2Path = "../AI/src/communication/play.py";

							new Thread(() -> {
                                Move moveBot2 = null;
                                try {
                                    moveBot2 = BotConnect.askAI(bot2Path, gameEngine);
                                } catch (IOException ex) {
                                    throw new RuntimeException(ex);
                                }

								Move finalMoveBot = moveBot2;
								javafx.application.Platform.runLater(() -> {
									if (finalMoveBot != null) {
										gameEngine.playMove(finalMoveBot);
										PieceMangee(gc,boardfx.getSpriteAt(finalMoveBot.end.y,finalMoveBot.end.x),finalMoveBot,boardfx);
										boardfx.updateMove(gameEngine.getBoard());
									}
								});
							}).start();
							break;
					}
					
					//affiche à qui c'est le tour
					
					if (gameEngine.getCurrentPlayer() == Color.WHITE) {
						gc.drawImage(white, l, -5);
					} else {
						gc.drawImage(black, l, -5);
					}
					moves = new ArrayList<>();
					gc.drawImage(rouge, 0, 0);
					
						
					
					
				}else {
					boardfx.selectedSprite=null;
					moves = new ArrayList<>();
					gc.drawImage(rouge, 0, 0);
					
					
					
				}
			
			}
			
		});
		
		
		//actualise les sprite à entre chaque coup
		AnimationTimer at = new AnimationTimer() {
			@Override
			public void handle(long lo) {
				if (boardfx.typeMatch=="classic") {
					if (gameEngine.getCurrentPlayer()==Color.BLACK) {
						gc.drawImage(fond, 0, 0);
					} else {
						gc.drawImage(fondNoir, 0, 0);
					}
				}else {
					gc.drawImage(fond, 0, 0);
				}
				for (int i=0;i<8;i++) {
		    		for (int j=0;j<8;j++) {
		    			if (boardfx.getArray()[i][j]!=null) {
		    				
		    				Sprite sprite= boardfx.getArray()[i][j];
		    				if (boardfx.typeMatch=="classic") {
			    				if (gameEngine.getCurrentPlayer()==Color.BLACK) {
			    					sprite.renderBlack(gc);
			    				} else {
			    					sprite.render(gc);
			    				}
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
				gc.drawImage(blanc, 9*l+10, l);
				gc.drawImage(blanc, 9*l+10, 7*l);
				int nb_Noir =0;
				Iterator<Sprite> itnoir = listeMangeeNoir.iterator();

				while (itnoir.hasNext()) {
				    Sprite sprite = itnoir.next();				    
				    if (gameEngine.getCurrentPlayer()==Color.BLACK) {
    					sprite.setPosition(9*l+nb_Noir*l/3, 7*l);
    					sprite.render(gc);
    				} else {
    					sprite.setPosition(9*l+nb_Noir*l/3, l);
    					sprite.render(gc);
    				}
				    nb_Noir++;
				}
				int nb_Blanc =0;
				Iterator<Sprite> itblanc = listeMangeeBlanc.iterator();

				while (itblanc.hasNext()) {
				    Sprite sprite = itblanc.next();				    
				    if (gameEngine.getCurrentPlayer()==Color.BLACK) {
    					sprite.setPosition(9*l+nb_Blanc*l/3, l);
    					sprite.render(gc);
    				} else {
    					sprite.setPosition(9*l+nb_Blanc*l/3, 7*l);
    					sprite.render(gc);
    				}
				    nb_Blanc++;
				}

				
				
			}
		};
		at.start();
	}
	//ajoute les pieces mangees aux diffrentes liste
	public void PieceMangee(GraphicsContext gc,Sprite next,Move move,BoardFX boardfx) {
		if (next!=  null) {
			Image piece_mangee = next.image;
			if (gameEngine.getCurrentPlayer()==Color.BLACK) {
				Sprite sprite = new Sprite(piece_mangee.getUrl(),l/2);
				listeMangeeBlanc.add(sprite);
				
			} else {
				Sprite sprite = new Sprite(piece_mangee.getUrl(),l/2);
				listeMangeeNoir.add(sprite);
			}
			
		}else { if (gameEngine.getBoard()[move.end.x][move.end.y] instanceof Pawn) {
        	if (move.start.y!=move.end.y) {
        		int dx = move.start.x -move.end.x;
        		
        		Image piece_mangee_en_passant = boardfx.getSpriteAt(move.end.y ,move.end.x+dx).image;
        		
        		if (gameEngine.getCurrentPlayer()==Color.BLACK) {
        			Sprite sprite = new Sprite(piece_mangee_en_passant.getUrl(),l/2);
    				listeMangeeBlanc.add(sprite);
				} else {
					Sprite sprite = new Sprite(piece_mangee_en_passant.getUrl(),l/2);
					listeMangeeBlanc.add(sprite);
				}
        		      			
        	}
        }
			
		}
	}
	//transforme des coordonnees de souris en case de l'echequier 
	public static Position doubleToPosition(double x, double y) {
		return new Position((int)(x/l)*l,(int)(y/l)*l);
	}
	public static void main(String[] args) {
		
		launch(args);
	}
}

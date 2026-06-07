package logic.utils;

import logic.game.GameEngine;
import logic.game.Move;
import logic.game.Position;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class BotConnect {

    /**
     * Appelle le bot pour récupérer un coup
     * @param path Chemin vers main.py
     * @param game Partie en cours
     * @return le coup à jouer
     */
    public static Move getBestMove(String path, GameEngine game) {

        String fen = FenConversion.toFen(game);

        try {
            // Commande
            List<String> command = new ArrayList<>();
            command.add("python3");
            command.add(path);
            System.out.println("Script : " + Paths.get(path).toAbsolutePath());
            command.add(fen);

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true);
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            String bestMove = null;
            while ((line = reader.readLine()) != null) {
                if (!line.trim().isEmpty()) {
                    bestMove = line.trim();
                }
            }

            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.err.println("Erreur Python : " + exitCode);
            }

            String startSquare = bestMove.substring(0, 2); // "e2"
            String endSquare = bestMove.substring(2, 4);   // "e4"
            
            System.out.println(startSquare);
            System.out.println(endSquare);
            
            
            Position startPos = AlgebraicNotation.toCoordinates(startSquare);
            Position endPos = AlgebraicNotation.toCoordinates(endSquare);
            return new Move(startPos, endPos);

        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
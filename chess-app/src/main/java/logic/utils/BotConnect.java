package logic.utils;

import logic.game.GameEngine;
import logic.game.Move;
import logic.game.Position;

import java.io.BufferedReader;
import java.io.IOException;
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
    public static Move getBestMove(String path, GameEngine game) throws IOException {

        String fen = FenConversion.toFen(game);

        // Commande
        List<String> command = new ArrayList<>();
        command.add("/home/lucky74/pytorchvenv/bin/python3");
        command.add(Paths.get(path).toAbsolutePath().toString());
        command.add(fen);

        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.redirectErrorStream(true);
        java.io.File scriptFile = new java.io.File(path).getAbsoluteFile();
        if (scriptFile.getParentFile() != null) {
            processBuilder.directory(scriptFile.getParentFile());
        }
        Process process = processBuilder.start();
        BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

        String line;
        String bestMove = null;

        while ((line = reader.readLine()) != null) {
            String trimmed = line.trim();
            if (!trimmed.isEmpty() && trimmed.length() == 4) {
                bestMove = trimmed;
            }
        }

        if (bestMove == null || bestMove.length() < 4) {
            return null;
        }

        String startSquare = bestMove.substring(0, 2);
        String endSquare = bestMove.substring(2, 4);

        Position startPos = AlgebraicNotation.toCoordinates(startSquare);
        Position endPos = AlgebraicNotation.toCoordinates(endSquare);
        return new Move(startPos, endPos);

    }
}
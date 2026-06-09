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
        System.out.println("[BOTCONNECT] FEN envoyé au bot : " + fen);

        try {
            // Commande
            List<String> command = new ArrayList<>();
            command.add("C:\\Users\\jerem\\git\\Projet-Developpement-Echecs\\venv-chess-ai\\bin\\python3");
            command.add(Paths.get(path).toAbsolutePath().toString());
            System.out.println("[BOTCONNECT] Exécution du script : " + Paths.get(path).toAbsolutePath());
            command.add(fen);

            ProcessBuilder processBuilder = new ProcessBuilder(command);
            processBuilder.redirectErrorStream(true);
            java.io.File scriptFile = new java.io.File(path).getAbsoluteFile();
            if (scriptFile.getParentFile() != null) {
                processBuilder.directory(scriptFile.getParentFile());
                System.out.println("[BOTCONNECT] Dossier de travail sur : " + scriptFile.getParentFile().getAbsolutePath());
            }
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            String line;
            String bestMove = null;

            System.out.println("[BOTCONNECT] --- Début des logs Python ---");
            while ((line = reader.readLine()) != null) {
                System.out.println("[PYTHON OUTPUT] " + line);
                String trimmed = line.trim();
                if (!trimmed.isEmpty() && trimmed.length() == 4) {
                    bestMove = trimmed;
                }
            }
            System.out.println("[BOTCONNECT] --- Fin des logs Python ---");

            int exitCode = process.waitFor();
            System.out.println("[BOTCONNECT] Code de sortie du processus Python : " + exitCode);

            if (exitCode != 0) {
                System.err.println("[BOTCONNECT] Le script Python s'est terminé avec une erreur (Code " + exitCode + ").");
            }

            if (bestMove == null || bestMove.length() < 4) {
                System.err.println("[BOTCONNECT] Erreur : Aucun coup valide n'a pu être extrait de Python.");
                return null;
            }

            String startSquare = bestMove.substring(0, 2);
            String endSquare = bestMove.substring(2, 4);

            System.out.println("[BOTCONNECT] Cases détectées -> Départ : " + startSquare + ", Arrivée : " + endSquare);

            Position startPos = AlgebraicNotation.toCoordinates(startSquare);
            Position endPos = AlgebraicNotation.toCoordinates(endSquare);
            return new Move(startPos, endPos);

        } catch (Exception e) {
            System.err.println("[BOTCONNECT] Une exception Java est survenue lors de l'appel du bot :");
            e.printStackTrace();
            return null;
        }
    }
}
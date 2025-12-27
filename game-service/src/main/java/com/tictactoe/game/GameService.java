package com.tictactoe.game;

import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Service
public class GameService {

    private final Random random = new Random();

    public int getNextMove(String board, int level) {
        // board is a string of length 9, e.g., "XO--X---O"
        // 'X' is Player, 'O' is AI (assumed for simplicity, or we can pass turn)
        // Let's assume AI is consistently 'O' and Player is 'X' for now, 
        // or we can determine based on count. 
        // Actually best to pass who is to move, but let's imply it.
        
        char aiPlayer = 'O';
        char humanPlayer = 'X';

        if (level <= 1) {
            return getRandomMove(board);
        } else if (level <= 3) {
            return getBasicMove(board, aiPlayer, humanPlayer);
        } else {
            return getMinimaxMove(board, aiPlayer, humanPlayer);
        }
    }

    private int getRandomMove(String board) {
        List<Integer> availableMoves = getAvailableMoves(board);
        if (availableMoves.isEmpty()) return -1;
        return availableMoves.get(random.nextInt(availableMoves.size()));
    }

    private int getBasicMove(String board, char ai, char human) {
        // 1. Check if can win
        int winMove = findWinningMove(board, ai);
        if (winMove != -1) return winMove;

        // 2. Check if need to block
        int blockMove = findWinningMove(board, human);
        if (blockMove != -1) return blockMove;

        // 3. Random
        return getRandomMove(board);
    }

    private int getMinimaxMove(String board, char ai, char human) {
        int bestScore = Integer.MIN_VALUE;
        int bestMove = -1;
        List<Integer> moves = getAvailableMoves(board);

        for (int move : moves) {
            String newBoard = makeMove(board, move, ai);
            int score = minimax(newBoard, 0, false, ai, human);
            if (score > bestScore) {
                bestScore = score;
                bestMove = move;
            }
        }
        return bestMove != -1 ? bestMove : getRandomMove(board);
    }

    private int minimax(String board, int depth, boolean isMaximizing, char ai, char human) {
        if (checkWin(board, ai)) return 10 - depth;
        if (checkWin(board, human)) return depth - 10;
        if (getAvailableMoves(board).isEmpty()) return 0;

        if (isMaximizing) {
            int bestScore = Integer.MIN_VALUE;
            for (int move : getAvailableMoves(board)) {
                String newBoard = makeMove(board, move, ai);
                int score = minimax(newBoard, depth + 1, false, ai, human);
                bestScore = Math.max(score, bestScore);
            }
            return bestScore;
        } else {
            int bestScore = Integer.MAX_VALUE;
            for (int move : getAvailableMoves(board)) {
                String newBoard = makeMove(board, move, human);
                int score = minimax(newBoard, depth + 1, true, ai, human);
                bestScore = Math.min(score, bestScore);
            }
            return bestScore;
        }
    }

    // Helper methods
    private List<Integer> getAvailableMoves(String board) {
        List<Integer> moves = new ArrayList<>();
        for (int i = 0; i < board.length(); i++) {
            if (board.charAt(i) == '-') moves.add(i);
        }
        return moves;
    }

    private String makeMove(String board, int index, char player) {
        char[] chars = board.toCharArray();
        chars[index] = player;
        return new String(chars);
    }

    private int findWinningMove(String board, char player) {
        for (int move : getAvailableMoves(board)) {
            String newBoard = makeMove(board, move, player);
            if (checkWin(newBoard, player)) return move;
        }
        return -1;
    }

    private boolean checkWin(String b, char p) {
        int[][] wins = {
            {0,1,2}, {3,4,5}, {6,7,8}, // Rows
            {0,3,6}, {1,4,7}, {2,5,8}, // Cols
            {0,4,8}, {2,4,6}           // Diags
        };
        for (int[] w : wins) {
            if (b.charAt(w[0]) == p && b.charAt(w[1]) == p && b.charAt(w[2]) == p) return true;
        }
        return false;
    }
}

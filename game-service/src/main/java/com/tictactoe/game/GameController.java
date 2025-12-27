package com.tictactoe.game;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/game")
public class GameController {

    @Autowired
    private GameService gameService;

    @GetMapping("/move")
    public ResponseEntity<Integer> getMove(@RequestParam String board, @RequestParam int level) {
        int move = gameService.getNextMove(board, level);
        return ResponseEntity.ok(move);
    }
}

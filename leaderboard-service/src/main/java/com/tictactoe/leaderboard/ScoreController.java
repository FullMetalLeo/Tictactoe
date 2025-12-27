package com.tictactoe.leaderboard;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/scores")
public class ScoreController {

    @Autowired
    private ScoreService scoreService;

    @PostMapping
    public ResponseEntity<Score> submitScore(@RequestParam String nickname, @RequestParam int points) {
        Score score = scoreService.submitScore(nickname, points);
        return ResponseEntity.ok(score);
    }

    @GetMapping
    public ResponseEntity<List<Score>> getLeaderboard() {
        return ResponseEntity.ok(scoreService.getLeaderboard());
    }
}

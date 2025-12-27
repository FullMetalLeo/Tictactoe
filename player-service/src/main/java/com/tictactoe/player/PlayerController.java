package com.tictactoe.player;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/players")
public class PlayerController {

    @Autowired
    private PlayerService playerService;

    @PostMapping
    public ResponseEntity<Player> createPlayer(@RequestParam String nickname) {
        Player player = playerService.createOrGetPlayer(nickname);
        return ResponseEntity.ok(player);
    }

    @GetMapping("/{nickname}")
    public ResponseEntity<Player> getPlayer(@PathVariable String nickname) {
        Player player = playerService.getPlayer(nickname);
        if (player != null) {
            return ResponseEntity.ok(player);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}

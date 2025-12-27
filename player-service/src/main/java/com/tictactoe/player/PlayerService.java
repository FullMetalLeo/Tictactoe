package com.tictactoe.player;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
public class PlayerService {

    @Autowired
    private PlayerRepository playerRepository;

    public Player createOrGetPlayer(String nickname) {
        Optional<Player> existingPlayer = playerRepository.findByNickname(nickname);
        return existingPlayer.orElseGet(() -> playerRepository.save(new Player(nickname)));
    }

    public Player getPlayer(String nickname) {
        return playerRepository.findByNickname(nickname).orElse(null);
    }
}

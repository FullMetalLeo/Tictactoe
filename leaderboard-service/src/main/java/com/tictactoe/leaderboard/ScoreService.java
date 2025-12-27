package com.tictactoe.leaderboard;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class ScoreService {

    @Autowired
    private ScoreRepository scoreRepository;

    public Score submitScore(String nickname, int points) {
        Score existingScore = scoreRepository.findByNickname(nickname);
        if (existingScore != null) {
            existingScore.setScore(existingScore.getScore() + points);
            return scoreRepository.save(existingScore);
        } else {
            return scoreRepository.save(new Score(nickname, points));
        }
    }

    public List<Score> getLeaderboard() {
        return scoreRepository.findAllByOrderByScoreDesc();
    }
}

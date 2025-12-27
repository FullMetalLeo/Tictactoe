package com.tictactoe.leaderboard;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.hamcrest.Matchers.hasSize;

@SpringBootTest
@AutoConfigureMockMvc
public class LeaderboardServiceTests {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testSubmitScore() throws Exception {
        mockMvc.perform(post("/scores")
                .param("nickname", "Winner")
                .param("points", "2"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.score").value(2));
    }

    @Test
    public void testLeaderboardOrder() throws Exception {
        // Submit low score
        mockMvc.perform(post("/scores").param("nickname", "Low").param("points", "1"));
        // Submit high score
        mockMvc.perform(post("/scores").param("nickname", "High").param("points", "50"));

        mockMvc.perform(get("/scores"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(2)))
                .andExpect(jsonPath("$[0].nickname").value("High")); // Highest first
    }
    
    @Test
    public void testScoreUpdate() throws Exception {
        // Initial
        mockMvc.perform(post("/scores").param("nickname", "Updater").param("points", "10"));
        
        // Add more
        mockMvc.perform(post("/scores").param("nickname", "Updater").param("points", "5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.score").value(15));
    }
}

package com.tictactoe.player;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;

@SpringBootTest
@AutoConfigureMockMvc
public class PlayerServiceTests {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testCreatePlayer() throws Exception {
        mockMvc.perform(post("/players").param("nickname", "TestUser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nickname").value("TestUser"));
    }

    @Test
    public void testGetPlayer() throws Exception {
        // Create first
        mockMvc.perform(post("/players").param("nickname", "ExistingUser"));

        // Then get
        mockMvc.perform(get("/players/ExistingUser"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.nickname").value("ExistingUser"));
    }

    @Test
    public void testGetNonExistentPlayer() throws Exception {
        mockMvc.perform(get("/players/Ghost"))
                .andExpect(status().isNotFound());
    }
}

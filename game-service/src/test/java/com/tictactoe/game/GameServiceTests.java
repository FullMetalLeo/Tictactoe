package com.tictactoe.game;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.junit.jupiter.api.Assertions.assertEquals;

@SpringBootTest
@AutoConfigureMockMvc
public class GameServiceTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private GameService gameService;

    @Test
    public void testMoveEndpoint() throws Exception {
        mockMvc.perform(get("/game/move")
                .param("board", "---------")
                .param("level", "1"))
                .andExpect(status().isOk());
    }

    @Test
    public void testMinimaxBlock() {
        // Human (X) is about to win: XX-
        // AI (O) should block
        String board = "XX-------";
        // 0 1 2
        // 3 4 5
        // 6 7 8
        // X at 0, 1. AI should pick 2.

        // However, GameService assumes AI is consistently 'O' or maximizing player.
        // And checks valid moves.
        // Let's trace getBasicMove or Minimax behavior.

        // NOTE: In current implementation, if level=3, it checks
        // "findWinningMove(board, human)" to block.
        // Human is 'X'. AI is 'O'.

        int move = gameService.getNextMove(board, 3);
        assertEquals(2, move, "AI Level 3 should block the winning move at index 2");
    }

    @Test
    public void testMinimaxWin() {
        // AI (O) is about to win: OO-
        String board = "OO-------";
        int move = gameService.getNextMove(board, 3);
        assertEquals(2, move, "AI Level 3 should take the winning move at index 2");
    }

    @Test
    public void testUnbeatableLevel() {
        // Testing full minimax (Level 5)
        // Board:
        // X O X
        // O O -
        // X X -
        //
        // 0:X, 1:O, 2:X
        // 3:O, 4:O, 5:- (Target Win)
        // 6:X, 7:X, 8:- (Danger)
        //
        // If AI is O, it has 4, and 1,3. Next move at 5 wins [3,4,5].
        // Move at 8 blocks X, but winning is priority.

        String board = "XOXOO-XX-";
        int move = gameService.getNextMove(board, 5);
        assertEquals(5, move, "AI Level 5 should prioritize winning immediately");
    }
}

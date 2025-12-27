import pygame
import requests
from core.constants import *
from core.renderer import SketchRenderer
from core.elements import Button, InputField

class TicTacToeClient:
    def __init__(self, screen):
        self.screen = screen
        self.renderer = SketchRenderer(screen)
        self.font_title = pygame.font.SysFont("Verdana", 60, bold=True) # Basic font fallback
        self.font_ui = pygame.font.SysFont("Verdana", 30)
        
        self.state = "MENU"
        self.mode = None # "SINGLE" or "PVP"
        self.level = 1
        self.board = ["-"] * 9
        self.turn = "X"
        self.winner = None
        
        self.p1_name = "Player 1"
        self.p2_name = "AI" # or Player 2

        self.setup_ui()

    def setup_ui(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Menu Elements
        self.btn_single = Button(pygame.Rect(cx - 150, cy - 50, 300, 60), "Single Player", self.font_ui, lambda: self.set_mode("SINGLE"))
        self.btn_pvp = Button(pygame.Rect(cx - 150, cy + 30, 300, 60), "PVP (Hotseat)", self.font_ui, lambda: self.set_mode("PVP"))
        self.btn_leaderboard = Button(pygame.Rect(cx - 150, cy + 110, 300, 60), "Leaderboard", self.font_ui, lambda: self.set_state("LEADERBOARD"))

        # Level Select Elements
        self.level_buttons = []
        for i in range(1, 6):
            rect = pygame.Rect(cx - 250 + (i-1)*100, cy, 80, 60)
            self.level_buttons.append(Button(rect, str(i), self.font_ui, lambda l=i: self.start_single_player(l)))

        # Game Over Elements
        self.btn_menu = Button(pygame.Rect(cx - 150, cy + 100, 300, 60), "Main Menu", self.font_ui, lambda: self.set_state("MENU"))

        # Input Fields (Simplified for now)
        self.input_p1 = InputField(pygame.Rect(cx - 150, cy - 100, 300, 50), self.font_ui, "Player 1")
        self.input_p2 = InputField(pygame.Rect(cx - 150, cy, 300, 50), self.font_ui, "Player 2")
        self.btn_start_pvp = Button(pygame.Rect(cx - 150, cy + 100, 300, 60), "Start PVP", self.font_ui, self.start_pvp)

    def set_mode(self, mode):
        self.mode = mode
        if mode == "SINGLE":
            self.state = "LEVEL_SELECT"
        else:
            self.state = "PLAYER_SETUP"

    def set_state(self, state):
        self.state = state

    def start_single_player(self, level):
        self.level = level
        self.p1_name = "You"
        self.p2_name = "AI (Lvl {})".format(level)
        self.reset_game()
        self.state = "GAME"

    def start_pvp(self):
        self.p1_name = self.input_p1.text
        self.p2_name = self.input_p2.text
        self.reset_game()
        self.state = "GAME"

    def reset_game(self):
        self.board = ["-"] * 9
        self.turn = "X"
        self.winner = None

    def handle_event(self, event):
        if self.state == "MENU":
            self.btn_single.handle_event(event)
            self.btn_pvp.handle_event(event)
            self.btn_leaderboard.handle_event(event)
        
        elif self.state == "LEVEL_SELECT":
            for btn in self.level_buttons:
                btn.handle_event(event)

        elif self.state == "PLAYER_SETUP":
            self.input_p1.handle_event(event)
            self.input_p2.handle_event(event)
            self.btn_start_pvp.handle_event(event)

        elif self.state == "GAME":
            if not self.winner and event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == "SINGLE" and self.turn == "O":
                    return # Wait for AI
                
                # Check grid click
                mx, my = event.pos
                board_rect = self.get_board_rect()
                if board_rect.collidepoint(mx, my):
                    cell_size = board_rect.width // 3
                    col = (mx - board_rect.x) // cell_size
                    row = (my - board_rect.y) // cell_size
                    index = row * 3 + col
                    if self.board[index] == "-":
                        self.make_move(index)

        elif self.state == "GAME_OVER":
            self.btn_menu.handle_event(event)
        
        elif self.state == "LEADERBOARD":
             if event.type == pygame.MOUSEBUTTONDOWN:
                 self.set_state("MENU") # Click anywhere to go back

    def update(self):
        if self.state == "GAME" and self.mode == "SINGLE" and self.turn == "O" and not self.winner:
            # AI Move
            try:
                board_str = "".join(self.board)
                url = f"http://localhost:8083/game/move?board={board_str}&level={self.level}"
                response = requests.get(url)
                if response.status_code == 200:
                    move = response.json()
                    if move != -1:
                        self.make_move(move)
            except:
                pass # Handle error gracefully

    def make_move(self, index):
        self.board[index] = self.turn
        if self.check_win(self.turn):
            self.winner = self.turn
            self.end_game()
        elif "-" not in self.board:
            self.winner = "Draw"
            self.end_game()
        else:
            self.turn = "O" if self.turn == "X" else "X"

    def check_win(self, p):
        wins = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        return any(all(self.board[i] == p for i in w) for w in wins)

    def end_game(self):
        self.state = "GAME_OVER"
        # Submit Score Logic here
        if self.winner == "X":
            self.submit_score(self.p1_name, 2)
        elif self.winner == "O" and self.mode == "PVP":
             self.submit_score(self.p2_name, 2)
        elif self.winner == "Draw":
             self.submit_score(self.p1_name, 1)
             if self.mode == "PVP":
                 self.submit_score(self.p2_name, 1)

    def submit_score(self, name, points):
        try:
            requests.post(f"http://localhost:8082/scores?nickname={name}&points={points}")
        except:
            print("Failed to submit score")

    def draw(self):
        self.screen.fill(COLOR_PAPER_WHITE)
        
        if self.state == "MENU":
            title = self.font_title.render("Tic-Tac-Toe", True, COLOR_PENCIL_BLACK)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))
            self.btn_single.draw(self.renderer)
            self.btn_pvp.draw(self.renderer)
            self.btn_leaderboard.draw(self.renderer)

        elif self.state == "LEVEL_SELECT":
            title = self.font_ui.render("Select AI Level", True, COLOR_PENCIL_BLACK)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 200)))
            for btn in self.level_buttons:
                btn.draw(self.renderer)

        elif self.state == "PLAYER_SETUP":
             title = self.font_ui.render("Enter Nicknames", True, COLOR_PENCIL_BLACK)
             self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 100)))
             self.input_p1.draw(self.renderer)
             self.input_p2.draw(self.renderer)
             self.btn_start_pvp.draw(self.renderer)

        elif self.state == "GAME" or self.state == "GAME_OVER":
            self.draw_board()
            turn_text = f"Turn: {self.p1_name if self.turn == 'X' else self.p2_name}"
            if self.winner:
                turn_text = "Winner: " + (self.winner if self.winner == "Draw" else (self.p1_name if self.winner == 'X' else self.p2_name))
            
            lbl = self.font_ui.render(turn_text, True, COLOR_PENCIL_BLACK)
            self.screen.blit(lbl, (50, 50))
            
            if self.state == "GAME_OVER":
                self.btn_menu.draw(self.renderer)

        elif self.state == "LEADERBOARD":
             self.draw_leaderboard()

    def get_board_rect(self):
        size = 400
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        return pygame.Rect(cx - size//2, cy - size//2, size, size)

    def draw_board(self):
        rect = self.get_board_rect()
        # Draw grid
        cell = rect.width // 3
        # Vertical
        self.renderer.draw_line_rough(COLOR_PENCIL_BLACK, (rect.x + cell, rect.y), (rect.x + cell, rect.bottom))
        self.renderer.draw_line_rough(COLOR_PENCIL_BLACK, (rect.x + 2*cell, rect.y), (rect.x + 2*cell, rect.bottom))
        # Horizontal
        self.renderer.draw_line_rough(COLOR_PENCIL_BLACK, (rect.x, rect.y + cell), (rect.right, rect.y + cell))
        self.renderer.draw_line_rough(COLOR_PENCIL_BLACK, (rect.x, rect.y + 2*cell), (rect.right, rect.y + 2*cell))

        # Draw Symbols
        for i in range(9):
             row, col = divmod(i, 3)
             x = rect.x + col * cell
             y = rect.y + row * cell
             sym = self.board[i]
             if sym == "X":
                 self.renderer.draw_x(COLOR_PENCIL_BLUE, (x, y, cell, cell))
             elif sym == "O":
                 self.renderer.draw_o(COLOR_PENCIL_RED, (x, y, cell, cell))

    def draw_leaderboard(self):
        title = self.font_title.render("Leaderboard", True, COLOR_PENCIL_BLACK)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 50)))
        
        try:
            scores = requests.get("http://localhost:8082/scores").json()
            y = 150
            for i, s in enumerate(scores[:10]):
                text = f"{i+1}. {s['nickname']}: {s['score']}"
                lbl = self.font_ui.render(text, True, COLOR_PENCIL_BLACK)
                self.screen.blit(lbl, (SCREEN_WIDTH//2 - 100, y))
                y += 40
        except:
            lbl = self.font_ui.render("Failed to load scores", True, COLOR_PENCIL_RED)
            self.screen.blit(lbl, (SCREEN_WIDTH//2 - 100, 150))
            
        hint = self.font_ui.render("Click anywhere to return", True, COLOR_PENCIL_BLACK)
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50)))

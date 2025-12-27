import pygame
import sys
from core.constants import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

from game_client import TicTacToeClient

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = TicTacToeClient(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                 screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                 game.screen = screen
                 game.renderer.screen = screen
            
            game.handle_event(event)

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

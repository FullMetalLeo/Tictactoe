import pygame
from core.constants import *

class UIElement:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        return False

    def draw(self, renderer):
        pass

class Button(UIElement):
    def __init__(self, rect, text, font, action=None):
        super().__init__(rect)
        self.text = text
        self.font = font
        self.action = action

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

    def draw(self, renderer):
        color = COLOR_PENCIL_RED if self.hovered else COLOR_PENCIL_BLACK
        renderer.draw_rect_rough(color, self.rect)
        
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        renderer.screen.blit(text_surface, text_rect)

class InputField(UIElement):
    def __init__(self, rect, font, initial_text=""):
        super().__init__(rect)
        self.text = initial_text
        self.font = font
        self.active = False

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # self.active = False # Optional: Keep active
                pass
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False

    def draw(self, renderer):
        color = COLOR_PENCIL_BLUE if self.active else COLOR_PENCIL_BLACK
        renderer.draw_rect_rough(color, self.rect)
        
        text_surface = self.font.render(self.text, True, color)
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        renderer.screen.blit(text_surface, text_rect)

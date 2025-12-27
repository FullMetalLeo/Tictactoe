import pygame
import random
import math

class SketchRenderer:
    def __init__(self, screen):
        self.screen = screen

    def _jitter(self, val, amount=2):
        return val + random.uniform(-amount, amount)

    def draw_line_rough(self, color, start_pos, end_pos, width=2):
        # Draw multiple lines to simulate pencil strokes
        for _ in range(2):
            s = (self._jitter(start_pos[0]), self._jitter(start_pos[1]))
            e = (self._jitter(end_pos[0]), self._jitter(end_pos[1]))
            pygame.draw.line(self.screen, color, s, e, width)

    def draw_rect_rough(self, color, rect, width=2):
        x, y, w, h = rect
        points = [
            (x, y), (x + w, y),
            (x + w, y + h), (x, y + h),
            (x, y) # Close loop
        ]
        for i in range(len(points) - 1):
            self.draw_line_rough(color, points[i], points[i+1], width)

    def draw_circle_rough(self, color, center, radius, width=2):
        # Approximate circle with lines
        points = []
        num_segments = 12
        for i in range(num_segments + 1):
            angle = (i / num_segments) * 2 * math.pi
            px = center[0] + math.cos(angle) * radius
            py = center[1] + math.sin(angle) * radius
            points.append((px, py))
        
        for i in range(len(points) - 1):
            self.draw_line_rough(color, points[i], points[i+1], width)

    def draw_x(self, color, rect, width=4):
        x, y, w, h = rect
        # Draw two crossing lines
        self.draw_line_rough(color, (x + 10, y + 10), (x + w - 10, y + h - 10), width)
        self.draw_line_rough(color, (x + w - 10, y + 10), (x + 10, y + h - 10), width)

    def draw_o(self, color, rect, width=4):
        x, y, w, h = rect
        center = (x + w // 2, y + h // 2)
        radius = min(w, h) // 2 - 10
        self.draw_circle_rough(color, center, radius, width)

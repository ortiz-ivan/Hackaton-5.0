import pygame


class StateManager:
    def __init__(self, game):
        self.game = game
        self.current_state = "PLAYING"

    def is_game_over(self):
        return self.current_state == "GAME_OVER"

    def render(self, screen):
        if self.current_state == "GAME_OVER":
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (200, 250))

import pygame
from core.game import Game
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Nombre del juego")
    clock = pygame.time.Clock()

    game = Game(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000
        running = game.update(dt)
        game.render()

    pygame.quit()


if __name__ == "__main__":
    main()

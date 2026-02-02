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
        dt = clock.tick(FPS) / 1000  # delta time en segundos

        # --- Procesar eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Actualización ---
        game.update(
            dt
        )  # aquí se actualizan todos los sistemas: input, movimiento, spawn, interacción, caos

        # --- Render ---
        game.render()  # dibuja fondo, player, estudiantes, obstáculos, HUD

    pygame.quit()


if __name__ == "__main__":
    main()

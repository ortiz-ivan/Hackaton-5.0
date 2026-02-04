import pygame
from core.game import Game
from ui.menu import MenuInicial, Menu_GameOver, Menu_Pausa # <--- Importamos tus clases
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Definimos los estados posibles
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAMEOVER = "GAMEOVER"
STATE_PAUSE = "PAUSE"

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Lecture Rush") # Nombre actualizado
    clock = pygame.time.Clock()

    # --- INICIALIZACIÓN ---
    game = Game(screen)             # El juego (lógica de Iván/Gabriel)
    
    # Tus Menús (Tu trabajo)
    menu_inicial = MenuInicial(screen)
    menu_pausa = Menu_Pausa(screen)
    menu_gameover = Menu_GameOver(screen)

    current_state = STATE_MENU      # Empezamos en el menú, no en el juego

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # delta time en segundos
        dt = min(dt, 0.1) # <--- NUEVO: Si dt es mayor a 0.1, fórulalo a 0.1

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            # Tecla ESC para pausar (solo si estamos jugando)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if current_state == STATE_PLAYING:
                    current_state = STATE_PAUSE

        # --- LÓGICA DE ESTADOS (El Semáforo) ---
        
        # CASO 1: ESTAMOS EN EL MENÚ PRINCIPAL
        if current_state == STATE_MENU:
            action = menu_inicial.update(events) # Tu código detecta teclas
            menu_inicial.render()                # Tu código dibuja
            
            if action == "Jugar":
                current_state = STATE_PLAYING    # ¡Arranca el juego!
            elif action == "Salir":
                running = False

        # CASO 2: ESTAMOS JUGANDO (El código original que mandaste)
        elif current_state == STATE_PLAYING:
            game.update(dt)     # Actualiza alumnos, caos, etc.
            game.render()       # Dibuja el aula
            
            # (Opcional) Si el juego detecta Game Over internamente:
            # if game.is_game_over:
            #     current_state = STATE_GAMEOVER

        # CASO 3: ESTAMOS EN PAUSA
        elif current_state == STATE_PAUSE:
            # Opcional: dibujar el juego de fondo congelado antes del menú
            # game.render() 
            
            action = menu_pausa.update(events)
            menu_pausa.render()

            if action == "Reanudar":
                current_state = STATE_PLAYING
            elif action == "Salir":
                current_state = STATE_MENU
                game = Game(screen) # Reseteamos el juego al salir

        # CASO 4: GAME OVER
        elif current_state == STATE_GAMEOVER:
            action = menu_gameover.update(events)
            menu_gameover.render()

            if action == "Reiniciar":
                game = Game(screen) # Reiniciar el juego desde cero
                current_state = STATE_PLAYING
            elif action == "Salir":
                current_state = STATE_MENU

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

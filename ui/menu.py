import pygame
import sys

#Clase madre y configuracion general para los tres menus (INICIAL, PAUSA Y GAME OVER)
class Menu:
    def __init__(self, screen, titulo, opciones):
        self.screen = screen
        self.titulo = titulo
        self.opciones = opciones
        self.selected_index = 0

        self.font = pygame.font.Font("ui/fonts/early_gameboy.ttf", 48)
        self.title_font = pygame.font.Font("ui/fonts/early_gameboy.ttf", 50)

        self.color_normal = (200, 200, 200)
        self.color_selected = (255, 220, 100)
        self.bg_color = (30, 30, 40)

        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        center_x = self.screen.get_width() // 2
        start_y = self.screen.get_height() // 2

        for i, texto in enumerate(self.opciones):
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (center_x, start_y + i * 80)
            self.buttons.append((texto, rect))

    def render(self):
        self.screen.fill(self.bg_color)
        self._draw_title()
        self._draw_buttons()

    def _draw_title(self):
        title_surf = self.title_font.render(self.titulo, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_surf, title_rect)
    
    def _draw_buttons(self):
        for i, (texto, rect) in enumerate(self.buttons):
            color = self.color_selected if i == self.selected_index else self.color_normal

            pygame.draw.rect(self.screen, color, rect, border_radius=8)

            text_surf = self.font.render(texto, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)

                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)

                elif event.key == pygame.K_RETURN:
                    return self.opciones[self.selected_index]

#CREACION Y EJECUCION DEL MENU DE INICIO                       
class MenuInicial(Menu):
    def __init__(self, screen):
         super().__init__(
             screen,
             "Penguin Chaos",
             ["Jugar", "Salir"]
         )


def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Penguin Chaos")

    menu = MenuInicial(screen)

    running = True
    while running:
         events = pygame.event.get()
         for event in events:
             if event.type == pygame.QUIT:
                 running = False

         menu.update(events)
         menu.render()

         pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


#CREACION Y EJECUCION DEL MENU GAME OVER (al terminar el juego)
class Menu_GameOver(Menu):
    def __init__(self, screen):
        super().__init__(
            screen,
            "Game Over",
            ["Volver a jugar", "Salir"]
        )        

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Over")

    menu = Menu_GameOver(screen)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        menu.update(events)
        menu.render()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()


#CREACION Y EJECUCION DEL MENU PAUSA 
class Menu_Pausa(Menu):
    def __init__(self, screen):
        super().__init__(
            screen,
            "Juego en Pausa",
            ["Reanudar partida", "Salir"]
        )        

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Juego en Pausa")

    menu = Menu_Pausa(screen)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        menu.update(events)
        menu.render()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

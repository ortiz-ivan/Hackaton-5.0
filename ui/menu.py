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

# 116,103,193 LAVANDA / LILA CLARO
# 46,42,79 AZUL MARINO
# 243,181,47 AMARILLO CLARO
# 190,59,108 ROSA/MAGENTA 
# 229,33,46 ROSA ANARANJADO 
# 200,200,200 GRIS
# 30,30,40 AZUL GRISACEO 
# 255,255,255 BLANCO
        self.color_normal = (116,103,193)
        self.color_selected = (255,220,100)
        self.bg_color = (46,42,79)

        self.buttons = []
        self._create_buttons()
        
        #Para agregar un fondo 
        self.bg_image = pygame.image.load("ui/image/clouds_2.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (self.screen.get_width(), self.screen.get_height()))
        
        #Parametros de animacion para el fondo
        self.bg_x = 0
        self.bg_speed = 0.3

    def _create_buttons(self):
        center_x = self.screen.get_width() // 2
        start_y = self.screen.get_height() // 2

        for i, texto in enumerate(self.opciones):
            rect = pygame.Rect(0, 0, 450, 60) #LOS DOS ULTIMOS NUMEROS SON ANCHO Y ALTO RESPECTIVAMENTE
            rect.center = (center_x, start_y + i * 120) #DISTANCIA ENTRE LOS BOTONES
            self.buttons.append((texto, rect))

    def render(self):

        #self.screen.fill(self.bg_color) para ponerle un color al fondo

        #Para agregar una imagen de fondo
        self.screen.blit(self.bg_image, (0, 0)) 

        self.bg_x -= self.bg_speed
        if self.bg_x <= -self.screen.get_width():
            self.bg_x = 0
        self.screen.blit(self.bg_image, (self.bg_x, 0))
        self.screen.blit(self.bg_image, (self.bg_x + self.screen.get_width(), 0))

        self._draw_title()
        self._draw_buttons()


    def _draw_title(self):
        title_surf = self.title_font.render(self.titulo, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, 120))
        self.screen.blit(title_surf, title_rect)
    
    def _draw_buttons(self):
        for i, (texto, rect) in enumerate(self.buttons):
            # Color del botón
            if i == self.selected_index:
                # Parpadeo cada 500ms
                color = (255, 220, 100) if pygame.time.get_ticks() % 500 < 250 else (243, 181, 47)
            else:
                color = self.color_normal

            # Animación de tamaño del botón 
            draw_rect = rect.copy()  # no tocamos el rect original
            if i == self.selected_index:
                draw_rect.inflate_ip(10, 5)  # ancho +10, alto +5

            # Dibujar rectángulo 
            pygame.draw.rect(self.screen, color, draw_rect, border_radius=8)

            # Dibujar texto centrado 
            text_surf = self.font.render(texto, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=draw_rect.center)
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
            ["Reiniciar", "Salir"]
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
            ["Reanudar", "Salir"]
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

pygame.quit()
sys.exit()
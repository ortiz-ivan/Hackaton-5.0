import pygame
import sys

#Clase general para el boton
class Boton_configuracion:
    def __init__(self, text, center_pos):
        self.text = text
        self.rect = pygame.Rect(0, 0, 300, 60)
        self.rect.center = center_pos

#Clase madre para los menu (habran tres, Menu inicial, menu pausa y menu game over)
class Menu:
    def __init__ (self, titulo, opcion1, opcion2):
        self.titulo=titulo
        self.opcion1=opcion1
        self.opcion2=opcion2

        self.font = pygame.font.Font(None, 48)
        self.color_normal = (200, 200, 200)
        self.color_selected = (255, 220, 100)
        self.bg_color = (30, 30, 40)
#Clases hijas
#1 Menu principal
class Menu_inicial(Menu):
    def opciones (self):
        print (self.titulo)
        print (self.opcion1)
        print(self.opcion2)


menu_principal= Menu_inicial('Penguin chaos', 'Jugar', 'Salir')
menu_principal.opciones()

#2 Menu PAUSA
class Menu_pausa (Menu):
    def opciones_pausa (self):
        print (self.titulo)
        print (self.opcion1)
        print(self.opcion2)

menu_pausa= Menu_pausa ('En pausa', 'Continuar partida', 'Salir')
menu_pausa.opciones_pausa()


#3 Menu GAME OVER
class Game_over (Menu):
    def mensaje_gameover (self):
        print (self.titulo)
        print (self.opcion1)
        print(self.opcion2)

menu_gameover= Game_over ('Game over', 'Felicidades, ganaste!', 'Gracias por jugar')
menu_gameover.mensaje_gameover()
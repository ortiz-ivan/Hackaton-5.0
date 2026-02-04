import pygame
import os

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        
        # --- FUENTES ---
        try:
            self.font = pygame.font.Font("ui/fonts/early_gameboy.ttf", 20)
            self.font_timer = pygame.font.Font("ui/fonts/early_gameboy.ttf", 32)
        except:
            self.font = pygame.font.Font(None, 24)
            self.font_timer = pygame.font.Font(None, 40)

        # --- CONFIGURACIÓN BARRA DE VIDA (30s) ---
        self.bar_width = 100
        self.bar_height = 12
        # La ubicamos en la esquina superior derecha, bajo los corazones
        self.bar_x = self.width - 125
        self.bar_y = 55 
        
        # --- IMAGEN DE VIDA (CORAZÓN) ---
        self.heart_img = None
        try:
            path = os.path.join("assets", "images", "heart.png")
            img = pygame.image.load(path).convert_alpha()
            self.heart_img = pygame.transform.scale(img, (30, 30))
        except:
            print("No se encontró heart.png, se usarán círculos.")

    def render(self, score, total_time):
        """
        score: Puntuación actual
        total_time: Tiempo restante de la partida
        """
        self._draw_score(score)
        self._draw_global_timer(total_time)

    def _draw_score(self, score):
        score_text = f"PUNTOS: {score:04d}"
        text_surf = self.font.render(score_text, True, (255, 255, 255))
        self.screen.blit(text_surf, (10, 10))

    def _draw_global_timer(self, seconds):
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        color = (255, 255, 255) if seconds > 10 else (255, 50, 50)
        
        time_text = f"{mins:02}:{secs:02}"
        text_surf = self.font_timer.render(time_text, True, color)
        text_rect = text_surf.get_rect(center=(self.width // 2, 25))
        self.screen.blit(text_surf, text_rect)

    def _draw_lives(self, lives):
        # Posición inicial de los corazones (Esquina superior derecha)
        start_x = self.width - 50
        y = 20
        
        # Dibujamos solo la cantidad de vidas actuales
        for i in range(lives):
            # Se dibujan de derecha a izquierda
            pos_x = start_x - (i * 35)
            
            if self.heart_img:
                self.screen.blit(self.heart_img, (pos_x, y))
            else:
                # Fallback: Círculos rojos si no hay imagen
                pygame.draw.circle(self.screen, (220, 20, 60), (pos_x + 15, y + 15), 12)

    def _draw_life_timer_bar(self, current, maximum):
        # Calculamos el ratio (de 1.0 a 0.0)
        ratio = max(0, min(1, current / maximum))
        
        # Color dinámico: cambia de verde a rojo según el tiempo
        if ratio > 0.5: color = (50, 200, 50)
        elif ratio > 0.2: color = (230, 200, 50)
        else: color = (255, 50, 50)

        # 1. Fondo de la barra (Gris oscuro)
        bg_rect = pygame.Rect(self.bar_x, self.bar_y, self.bar_width, self.bar_height)
        pygame.draw.rect(self.screen, (40, 40, 40), bg_rect)
        
        # 2. Relleno de la barra (se acorta según el tiempo)
        fill_width = int(self.bar_width * ratio)
        fill_rect = pygame.Rect(self.bar_x, self.bar_y, fill_width, self.bar_height)
        pygame.draw.rect(self.screen, color, fill_rect)
        
        # 3. Borde blanco fino
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect, 1)
# name_prompt.py
import pygame
import time

class NamePrompt:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 36)  # Para etiqueta
        self.button_font = pygame.font.Font(None, 28)  # Fuente más pequeña para el botón
        self.input_font = pygame.font.Font(None, 32)
        
        # Fondo del aviso con gradiente de negro a azul oscuro
        self.background = pygame.Surface((450, 220), pygame.SRCALPHA)
        for y in range(220):
            r = 10 + (20 - 10) * (y / 220)  # De negro (10, 10, 10) a azul oscuro (20, 50, 138)
            g = 10 + (50 - 10) * (y / 220)
            b = 10 + (138 - 10) * (y / 220)
            pygame.draw.line(self.background, (int(r), int(g), int(b)), (0, y), (450, y))
        
        # Campo de texto
        self.input_box = pygame.Rect(screen_width // 2 - 175, screen_height // 2 - 20, 350, 50)
        self.input_text = ""
        self.active = True
        self.color_active = (70, 130, 180, 128)  # Azul acero (steelblue) con 50% opacidad
        self.color_inactive = (70, 130, 180, 128)  # Mismo color para consistencia
        self.color = self.color_active  # Definimos self.color inicialmente
        self.input_bg_color = (15, 30, 74, 77)  # Más oscuro, similar al gradiente
        self.cursor_visible = True  # Para el parpadeo del cursor
        self.cursor_timer = time.time()  # Para controlar el parpadeo
        
        # Botón "Start Adventure" alargado
        self.check_rect = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 40, 160, 40)  # Alargado a 160
        self.check_base_color = (20, 50, 138)  # Azul oscuro
        self.check_mid_color = (30, 144, 255)  # Azul claro
        self.check_text_color = (173, 216, 230)  # Azul claro pálido (lightblue)
        self.check_hover = False
        
        # Botón "X" para cerrar en la esquina superior derecha
        self.close_rect = pygame.Rect(screen_width // 2 + 190, screen_height // 2 - 100, 30, 30)
        self.close_color = (100, 100, 100)  # Gris para la "X"
        self.close_hover = False

    def draw(self):
        # Fondo congelado del menú
        frozen_screen = self.screen.copy()
        self.screen.blit(frozen_screen, (0, 0))
        
        # Dibujar el aviso con gradiente negro-azul
        self.background_rect = self.background.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(self.background, self.background_rect)
        pygame.draw.rect(self.screen, (70, 130, 180, 128), self.background_rect, 3, border_radius=15)  # Borde azul acero
        
        # Etiqueta "Who are you? seedizen"
        prompt_text = self.font.render("Who are you? seedizen", True, (173, 216, 230))  # lightblue
        prompt_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Campo de texto
        pygame.draw.rect(self.screen, self.input_bg_color, self.input_box, border_radius=5)  # Fondo más oscuro
        pygame.draw.rect(self.screen, self.color, self.input_box, 2, border_radius=5)  # Borde
        txt_surface = self.input_font.render(self.input_text, True, (173, 216, 230))  # Texto lightblue
        placeholder = self.input_font.render("Enter your name", True, (135, 206, 235, 128)) if not self.input_text else None  # skyblue/50
        self.screen.blit(txt_surface, (self.input_box.x + 10, self.input_box.y + 10))
        if placeholder:
            self.screen.blit(placeholder, (self.input_box.x + 10, self.input_box.y + 10))
        
        # Línea parpadeante (cursor) cuando el campo está activo
        if self.active:
            current_time = time.time()
            if current_time - self.cursor_timer >= 0.5:  # Parpadea cada 0.5 segundos
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = current_time
            if self.cursor_visible:
                cursor_x = self.input_box.x + 10 + txt_surface.get_width() + 2
                cursor_y_start = self.input_box.y + 10
                cursor_y_end = self.input_box.y + self.input_box.height - 10
                pygame.draw.line(self.screen, (173, 216, 230), (cursor_x, cursor_y_start), (cursor_x, cursor_y_end), 2)
        
        # Botón "Start Adventure"
        self.draw_mystery_button(self.check_rect, "Start Adventure", self.check_hover)
        
        # Botón "X" para cerrar
        pygame.draw.rect(self.screen, self.close_color if not self.close_hover else (150, 150, 150), 
                         self.close_rect, border_radius=5)
        close_text = self.font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=self.close_rect.center)
        self.screen.blit(close_text, close_text_rect)
        
        pygame.display.flip()

    def draw_mystery_button(self, rect, text, hovered):
        gradient_surface = pygame.Surface((rect.width, rect.height))
        for x in range(rect.width):
            r = self.check_base_color[0] + (self.check_mid_color[0] - self.check_base_color[0]) * (x / rect.width)
            g = self.check_base_color[1] + (self.check_mid_color[1] - self.check_base_color[1]) * (x / rect.width)
            b = self.check_base_color[2] + (self.check_mid_color[2] - self.check_base_color[2]) * (x / rect.width)
            pygame.draw.line(gradient_surface, (int(r), int(g), int(b)), (x, 0), (x, rect.height))
        
        self.screen.blit(gradient_surface, (rect.x, rect.y))
        pygame.draw.rect(self.screen, self.check_mid_color, rect, 2, border_radius=15)
        
        # Usar fuente más pequeña para el botón
        text_surface = self.button_font.render(text, True, self.check_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        if hovered:
            line_y = rect.y + rect.height - 5
            pygame.draw.line(self.screen, self.check_text_color, (rect.x + 10, line_y), 
                            (rect.x + rect.width - 10, line_y), 2)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.input_box.collidepoint(mouse_pos):
                self.active = True
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
            
            if self.check_rect.collidepoint(mouse_pos) and self.input_text:
                self.check_hover = True
                return self.input_text
            
            if self.close_rect.collidepoint(mouse_pos):
                return "close"
        
        if event.type == pygame.MOUSEMOTION:
            self.check_hover = self.check_rect.collidepoint(pygame.mouse.get_pos())
            self.close_hover = self.close_rect.collidepoint(pygame.mouse.get_pos())
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.input_text:
                return self.input_text
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 20:
                    self.input_text += event.unicode
        
        return None
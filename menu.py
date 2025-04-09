# menu.py
import pygame

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 48)  # Tamaño mediano para texto
        
        try:
            self.background = pygame.image.load("assets/lobby.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error al cargar lobby.png: {e}")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((0, 100, 0))
        
        # Botones con diseño "MysteryButton" ajustados
        self.button_width = 180  # Mantenemos el ancho
        self.button_height = 50  # Reducimos la altura de 70 a 50
        self.button_y_offset = 35  # Bajamos 10 píxeles más (25 + 10)
        self.play_button_rect = pygame.Rect(self.screen_width // 2 - self.button_width // 2, 
                                            self.screen_height // 2 - 20 + self.button_y_offset, 
                                            self.button_width, self.button_height)
        self.exit_button_rect = pygame.Rect(self.screen_width // 2 - self.button_width // 2, 
                                            self.screen_height // 2 + 60 + self.button_y_offset, 
                                            self.button_width, self.button_height)
        self.button_base_color = (30, 27, 75)  # Aproximación a indigo-900 (#1E1B4B)
        self.button_mid_color = (30, 58, 138)  # Aproximación a blue-800 (#1E3A8A)
        self.button_text_color = (165, 243, 252)  # Cyan-200 (#A5F3FC)
        self.shadow_color = (67, 56, 202, 128)  # Indigo-700/50 para sombra en hover
        
        self.show_name_prompt = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        # Detectar si el mouse está sobre los botones
        mouse_pos = pygame.mouse.get_pos()
        play_hovered = self.play_button_rect.collidepoint(mouse_pos)
        exit_hovered = self.exit_button_rect.collidepoint(mouse_pos)
        
        # Dibujar botón Play
        self.draw_mystery_button(self.play_button_rect, "Play", play_hovered)
        
        # Dibujar botón Exit
        self.draw_mystery_button(self.exit_button_rect, "Exit", exit_hovered)
        
        pygame.display.flip()

    def draw_mystery_button(self, rect, text, hovered):
        # Simular gradiente (de izquierda a derecha: indigo-900 a blue-800)
        gradient_surface = pygame.Surface((rect.width, rect.height))
        for x in range(rect.width):
            r = self.button_base_color[0] + (self.button_mid_color[0] - self.button_base_color[0]) * (x / rect.width)
            g = self.button_base_color[1] + (self.button_mid_color[1] - self.button_base_color[1]) * (x / rect.width)
            b = self.button_base_color[2] + (self.button_mid_color[2] - self.button_base_color[2]) * (x / rect.width)
            pygame.draw.line(gradient_surface, (int(r), int(g), int(b)), (x, 0), (x, rect.height))
        
        # Efecto hover: sombra
        if hovered:
            shadow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(shadow_surface, self.shadow_color, (0, 0, rect.width + 20, rect.height + 20), border_radius=15)
            self.screen.blit(shadow_surface, (rect.x - 10, rect.y - 10))
        
        # Dibujar el botón
        self.screen.blit(gradient_surface, (rect.x, rect.y))
        pygame.draw.rect(self.screen, self.button_mid_color, rect, 2, border_radius=15)  # Borde
        
        # Texto
        text_surface = self.font.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Línea inferior en hover
        if hovered:
            line_y = rect.y + rect.height - 5
            pygame.draw.line(self.screen, self.button_text_color, (rect.x + 10, line_y), 
                            (rect.x + rect.width - 10, line_y), 2)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.play_button_rect.collidepoint(mouse_pos):
                self.show_name_prompt = True
                return "name_prompt"
            elif self.exit_button_rect.collidepoint(mouse_pos):
                return "exit"
        return None
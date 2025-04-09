# anuncio.py
import pygame

class Anuncio:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.active = False
        self.image = None
        self.close_button_rect = None
        self.close_button_text = None

        # Configuración del botón de cierre "X"
        self.close_button_size = 30
        self.close_button_color = (255, 0, 0)  # Rojo
        self.close_button_border_color = (200, 0, 0)
        self.close_button_text = pygame.font.Font(None, 24).render("X", True, (255, 255, 255))

    def load_image(self, attack_name):
        try:
            if attack_name == "airdrop":
                self.image = pygame.image.load("assets/anuncioairdrop.png")
            elif attack_name == "double_tap":
                self.image = pygame.image.load("assets/anunciodoubletap.png")
            elif attack_name == "yieldstorm":  # Cambiado de crypto_crash a yieldstorm
                self.image = pygame.image.load("assets/anuncioyieldstorm.png")
            else:
                raise FileNotFoundError(f"No se encontró imagen para el ataque {attack_name}")
            # Ajustar el tamaño de la imagen para que quepa en la pantalla (por ejemplo, 600x400)
            self.image = pygame.transform.scale(self.image, (600, 400))
        except pygame.error as e:
            print(f"Error al cargar la imagen del anuncio para {attack_name}: {e}")
            self.image = pygame.Surface((600, 400))
            self.image.fill((50, 50, 50))  # Fondo gris si falla la carga
            font = pygame.font.Font(None, 36)
            text = font.render(f"Imagen de {attack_name} no encontrada", True, (255, 255, 255))
            text_rect = text.get_rect(center=(300, 200))
            self.image.blit(text, text_rect)

        # Posicionar el botón de cierre en la esquina superior derecha de la imagen
        image_rect = self.image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.close_button_rect = pygame.Rect(
            image_rect.right - self.close_button_size - 10,
            image_rect.top + 10,
            self.close_button_size,
            self.close_button_size
        )
        self.active = True  # Activar el anuncio después de cargar la imagen

    def draw(self, screen):
        if not self.active or not self.image:
            return

        # Fondo oscuro semitransparente
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Dibujar la imagen del anuncio
        image_rect = self.image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        screen.blit(self.image, image_rect)

        # Dibujar el botón de cierre
        pygame.draw.rect(screen, self.close_button_color, self.close_button_rect)
        pygame.draw.rect(screen, self.close_button_border_color, self.close_button_rect, 2)
        close_text_rect = self.close_button_text.get_rect(center=self.close_button_rect.center)
        screen.blit(self.close_button_text, close_text_rect)

    def handle_events(self, event):
        if not self.active:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.close_button_rect.collidepoint(mouse_pos):
                self.active = False
                return True  # Indica que el anuncio se cerró
        return False
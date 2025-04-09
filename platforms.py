# platforms.py
import pygame

class Platform:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side
        self.visible = False

        if side == "left":
            try:
                self.image = pygame.image.load("assets/plataformaizquierda.png")
                self.image = pygame.transform.scale(self.image, (250, 150))  # Tamaño ajustado
            except pygame.error as e:
                print(f"Error al cargar plataformaizquierda.png: {e}")
                self.image = pygame.Surface((250, 150))
                self.image.fill((100, 100, 100))
        elif side == "right":
            try:
                self.image = pygame.image.load("assets/plataformaderecha.png")
                self.image = pygame.transform.scale(self.image, (250, 150))  # Tamaño ajustado
            except pygame.error as e:
                print(f"Error al cargar plataformaderecha.png: {e}")
                self.image = pygame.Surface((250, 150))
                self.image.fill((100, 100, 100))

    def set_visible(self, visible):
        self.visible = visible

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, (self.x - 125, self.y - 75))  # Centrado: mitad de 250 y 150
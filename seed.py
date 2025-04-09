# seed.py
import pygame

class Seed:
    def __init__(self, x, y, platform_y):
        self.x = x  # Posición inicial en x (donde muere el enemigo)
        self.y = y  # Posición inicial en y (donde muere el enemigo)
        self.platform_y = platform_y  # Posición y de la plataforma (donde caerá la seed)
        self.velocity_y = 0  # Velocidad inicial de caída
        self.gravity = 0.5  # Gravedad para simular la caída
        self.on_ground = False  # Indica si la seed ha tocado el suelo
        self.time_on_ground = 0  # Tiempo que lleva en el suelo (en frames)
        self.lifetime = 12  # 0.2 segundos a 60 FPS (0.2 * 60 = 12 frames)

        # Cargar la imagen de la seed
        try:
            self.image = pygame.image.load("assets/seeds.png")
            self.image = pygame.transform.scale(self.image, (20, 20))  # Escalar la imagen
        except pygame.error as e:
            print(f"Error al cargar la imagen de la seed: {e}")
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 215, 0))  # Amarillo como respaldo

    def update(self):
        if not self.on_ground:
            # Aplicar gravedad para simular la caída
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            # Verificar si la seed ha tocado la plataforma
            if self.y >= self.platform_y:
                self.y = self.platform_y
                self.on_ground = True
                self.velocity_y = 0

        if self.on_ground:
            # Incrementar el tiempo en el suelo
            self.time_on_ground += 1

    def draw(self, screen):
        screen.blit(self.image, (self.x - 10, self.y - 10))  # Centrar la imagen

    def should_remove(self):
        # La seed debe eliminarse si ha estado en el suelo más de 0.2 segundos
        return self.on_ground and self.time_on_ground >= self.lifetime
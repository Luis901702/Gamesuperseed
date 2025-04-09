# bullet.py
import pygame
import random
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, speed=10):
        self.x = x
        self.y = y
        self.speed = speed  # Velocidad de la bala (píxeles por frame)

        # Cargar las imágenes de las balas
        try:
            self.image1 = pygame.image.load("assets/shotseed.png")
            self.image1 = pygame.transform.scale(self.image1, (20, 20))  # Ajustar tamaño si es necesario
            self.image2 = pygame.image.load("assets/shotseed2.png")
            self.image2 = pygame.transform.scale(self.image2, (20, 20))
        except pygame.error as e:
            print(f"Error al cargar las imágenes de las balas: {e}")
            self.image1 = pygame.Surface((20, 20))
            self.image1.fill((255, 0, 0))  # Color de respaldo: rojo
            self.image2 = pygame.Surface((20, 20))
            self.image2.fill((0, 255, 0))  # Color de respaldo: verde

        # Seleccionar una imagen aleatoria
        self.image = random.choice([self.image1, self.image2])
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # Calcular la dirección hacia el enemigo
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
        else:
            self.dx = 0
            self.dy = 0

    def update(self):
        # Mover la bala
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with(self, enemy):
        # Verificar colisión con el enemigo
        enemy_rect = pygame.Rect(enemy.x - 50, enemy.y - 50, 100, 100)  # Aproximación del área del enemigo
        return self.rect.colliderect(enemy_rect)
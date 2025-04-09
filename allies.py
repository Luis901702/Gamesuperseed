# allies.py
import pygame
import random
from bullet import Bullet

class Ally:
    def __init__(self, x, y, ally_type="generic"):
        self.x = x
        self.y = y
        self.base_x = x  # Posición base para regresar
        self.base_y = y
        self.ally_type = ally_type

        # Definir propiedades según el tipo de aliado (usando las estadísticas de la tabla)
        if ally_type == "seedfi":
            self.attack_power = 5
            self.attack_interval = 2.5  # Intervalo en segundos
        elif ally_type == "bebop":
            self.attack_power = 8
            self.attack_interval = 2.3
        elif ally_type == "stryke":
            self.attack_power = 11
            self.attack_interval = 2.1
        elif ally_type == "velodrome":
            self.attack_power = 14
            self.attack_interval = 1.9
        elif ally_type == "ionic":
            self.attack_power = 17
            self.attack_interval = 1.7
        elif ally_type == "bulletx":
            self.attack_power = 20
            self.attack_interval = 1.5
        elif ally_type == "mintpad":
            self.attack_power = 23
            self.attack_interval = 1.3
        elif ally_type == "fractal":
            self.attack_power = 26
            self.attack_interval = 1.1
        elif ally_type == "dolomite":
            self.attack_power = 29
            self.attack_interval = 0.9
        elif ally_type == "marginzero":
            self.attack_power = 32
            self.attack_interval = 0.7
        else:
            self.attack_power = 2
            self.attack_interval = 1.0

        self.attack_speed = 1 / self.attack_interval  # Calcular velocidad inicial (ataques/s)
        self.attack_timer = 0

        # Cargar la imagen según el tipo de aliado
        try:
            if self.ally_type == "bebop":
                self.image = pygame.image.load("assets/bebop.png")
            elif self.ally_type == "seedfi":
                self.image = pygame.image.load("assets/seedfi.png")
            elif self.ally_type == "stryke":
                self.image = pygame.image.load("assets/stryke.png")
            elif self.ally_type == "velodrome":
                self.image = pygame.image.load("assets/velodrome.png")
            elif self.ally_type == "ionic":
                self.image = pygame.image.load("assets/ionic.png")
            elif self.ally_type == "bulletx":
                self.image = pygame.image.load("assets/bulletx.png")
            elif self.ally_type == "mintpad":
                self.image = pygame.image.load("assets/mintpad.png")
            elif self.ally_type == "fractal":
                self.image = pygame.image.load("assets/fractal.png")
            elif self.ally_type == "dolomite":
                self.image = pygame.image.load("assets/dolomite.png")
            elif self.ally_type == "marginzero":
                self.image = pygame.image.load("assets/marginzero.png")
            else:
                self.image = pygame.image.load("assets/ally.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
        except pygame.error as e:
            print(f"Error al cargar la imagen del aliado {self.ally_type}: {e}")
            self.image = pygame.Surface((100, 100))
            if self.ally_type == "bebop":
                self.image.fill((0, 102, 204))
            elif self.ally_type == "seedfi":
                self.image.fill((34, 139, 34))
            elif self.ally_type == "stryke":
                self.image.fill((255, 215, 0))
            elif self.ally_type == "velodrome":
                self.image.fill((128, 0, 128))
            elif self.ally_type == "ionic":
                self.image.fill((0, 255, 255))
            elif self.ally_type == "bulletx":
                self.image.fill((255, 0, 0))
            elif self.ally_type == "mintpad":
                self.image.fill((0, 255, 0))
            elif self.ally_type == "fractal":
                self.image.fill((255, 165, 0))
            elif self.ally_type == "dolomite":
                self.image.fill((139, 69, 19))
            elif self.ally_type == "marginzero":
                self.image.fill((105, 105, 105))
            else:
                self.image.fill((255, 255, 0))

        # Variables para el efecto de impulso
        self.recoil_timer = 0
        self.recoil_duration = 200
        self.recoil_distance = 15
        self.recoil_direction = 0

    def attack(self, enemy_x, enemy_y, dt):
        # Incrementar el temporizador en segundos (dt es el delta time en segundos)
        self.attack_timer += dt
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            self.recoil_timer = self.recoil_duration
            self.recoil_direction = random.choice([0, 10, -10])
            bullet = Bullet(self.x, self.y, enemy_x, enemy_y, speed=10)
            return bullet, self.attack_power
        return None, 0

    def draw(self, screen):
        self.update()
        screen.blit(self.image, (self.x - 50, self.y - 50))

    def update(self):
        if self.recoil_timer > 0:
            progress = self.recoil_timer / self.recoil_duration
            if progress > 0.5:
                offset = self.recoil_distance * (1 - progress) * 2
            else:
                offset = self.recoil_distance * progress * 2
            
            self.x = self.base_x + offset * (self.recoil_direction / 10 if self.recoil_direction != 0 else 0)
            
            self.recoil_timer -= 16
            if self.recoil_timer <= 0:
                self.x = self.base_x

    def upgrade_attack_power(self):
        self.attack_power += 1  # Aumentar daño en 1 por nivel

    def upgrade_attack_speed(self):
        self.attack_speed += 0.1  # Aumentar velocidad en 0.1 ataques/s por nivel
        self.attack_interval = 1 / self.attack_speed  # Recalcular intervalo
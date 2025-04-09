# enemy.py
import pygame
import random

class Enemy:
    def __init__(self, x, y, is_boss=False, level=1):
        self.x = x
        self.y = y
        self.level = level  # Nivel del juego, pasado desde game.py
        self.normal_enemies = ["enemy1.png", "enemy2.png", "enemy3.png", "enemy4.png", "spectre.png", "corrupted.png", "enemy5.png", "enemy6.png"]
        self.special_enemies = {
            "enemyeth.png": {"probability": 0.05, "ssc_reward": 15},
            "enemyeth2.png": {"probability": 0.02, "ssc_reward": 25},
            "enemyeth3.png": {"probability": 0.01, "ssc_reward": 50}
        }
        self.is_special = False
        self.is_boss = is_boss
        self.ssc_reward = 0  # Recompensa de SSC si es especial
        self.load_random_enemy()

        # Definir características según el tipo de enemigo
        if self.selected_enemy == "enemy5.png":
            self.max_health = 250
            self.damage = 4
            self.attack_speed = 4000
        elif self.selected_enemy == "enemy6.png":
            self.max_health = 300
            self.damage = 5
            self.attack_speed = 3000
        elif self.selected_enemy in self.special_enemies:
            # Estadísticas iniciales más altas para enemigos especiales
            self.max_health = 350
            self.damage = 6
            self.attack_speed = 3500
        else:
            self.max_health = 200
            self.damage = 3
            self.attack_speed = 5000

        # Ajustar estadísticas según el nivel del juego
        self.max_health += self.level * 10  # +10 de vida por nivel
        self.damage += self.level * 0.5     # +0.5 de daño por nivel
        self.health = self.max_health

        # Si es jefe, duplicar vida y daño
        if self.is_boss:
            self.max_health *= 2
            self.health = self.max_health
            self.damage *= 2

        self.last_attack = pygame.time.get_ticks()
        self.shrink_timer = 0
        self.shrink_duration = 200
        self.shrink_scale = 0.9
        self.original_image = self.image
        self.particles = []  # Solo partículas de destrucción

    def load_random_enemy(self):
        # Seleccionar un enemigo especial según las probabilidades
        r = random.random()
        cumulative_prob = 0
        for enemy, data in self.special_enemies.items():
            cumulative_prob += data["probability"]
            if r < cumulative_prob:
                self.selected_enemy = enemy
                self.is_special = True
                self.ssc_reward = data["ssc_reward"]
                break
        else:
            self.selected_enemy = random.choice(self.normal_enemies)
            self.is_special = False
            self.ssc_reward = 0

        try:
            self.image = pygame.image.load(f"assets/{self.selected_enemy}")
            self.image = pygame.transform.scale(self.image, (400, 400))
            self.original_image = self.image
            self.colors = self.extract_colors()
        except pygame.error as e:
            print(f"Error al cargar la imagen del enemigo {self.selected_enemy}: {e}")
            self.image = None
            self.radius = 80
            self.color = (255, 0, 0)
            self.original_image = None
            self.colors = [(255, 0, 0), (200, 0, 0)]

    def extract_colors(self):
        if not self.image:
            return [(255, 0, 0), (200, 0, 0)]
        colors = []
        small_image = pygame.transform.scale(self.image, (10, 10))
        for x in range(10):
            for y in range(10):
                color = small_image.get_at((x, y))
                if color.a > 50 and color not in colors:
                    colors.append((color.r, color.g, color.b))
        return colors[:5] if colors else [(255, 0, 0), (200, 0, 0)]

    def draw(self, screen):
        self.update()
        if self.image:
            image_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, image_rect)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.shrink_timer = self.shrink_duration

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack >= self.attack_speed:
            self.last_attack = current_time
            return self.damage
        return 0

    def is_alive(self):
        return self.health > 0

    def reset(self, is_boss=False, level=1):
        if not self.is_special:
            print("Generando partículas de destrucción para enemigo normal")
            self.generate_destruction_particles()
        self.level = level  # Actualizar el nivel del juego
        self.max_health = 200 + random.randint(0, 50)  # Vida base entre 200 y 250
        self.damage = 3 + random.randint(0, 3)         # Daño base entre 3 y 6
        self.is_boss = is_boss

        # Ajustar estadísticas según el nivel del juego
        self.max_health += self.level * 10  # +10 de vida por nivel
        self.damage += self.level * 0.5     # +0.5 de daño por nivel
        self.health = self.max_health

        # Si es jefe, duplicar vida y daño
        if self.is_boss:
            self.max_health *= 2
            self.health = self.max_health
            self.damage *= 2

        self.load_random_enemy()

    def generate_destruction_particles(self):
        print(f"Creando {len(self.particles)} partículas iniciales -> 40 nuevas")
        for _ in range(40):
            color = random.choice(self.colors)
            radius = random.randint(5, 9)
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            self.particles.append({
                "x": self.x + random.randint(-80, 80),
                "y": self.y + random.randint(-80, 80),
                "dx": dx,
                "dy": dy,
                "radius": radius,
                "color": color,
                "life": 200
            })
        print(f"Total de partículas tras generar: {len(self.particles)}")

    def update(self):
        if self.shrink_timer > 0 and self.image:
            progress = self.shrink_timer / self.shrink_duration
            if progress > 0.5:
                scale = 1 - (1 - self.shrink_scale) * (1 - progress) * 2
            else:
                scale = self.shrink_scale + (1 - self.shrink_scale) * progress * 2
            new_size = (int(400 * scale), int(400 * scale))
            self.image = pygame.transform.scale(self.original_image, new_size)
            self.shrink_timer -= 16
            if self.shrink_timer <= 0:
                self.image = self.original_image
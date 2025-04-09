# heroe.py
import pygame
import random

class Heroe:
    def __init__(self, x, y):
        self.base_x = x  # Posición base en x
        self.base_y = y  # Posición base en y
        self.x = x  # Posición actual en x
        self.y = y  # Posición actual en y
        self.max_health = 100
        self.health = self.max_health
        self.attack_power = 10.0  # Daño base
        self.attack_speed = 1.0   # Factor de velocidad de ataque
        self.last_attack = 0
        self.level = 1
        self.recoil_direction = 0
        self.recoil_speed = 5
        self.recoil_duration = 100
        self.recoil_timer = 0

        # Nuevas propiedades para las mecánicas
        self.critical_multiplier = 1.8  # Multiplicador de daño crítico (80% inicial)
        self.critical_chance = 0.0      # Probabilidad de crítico (0% inicial)
        self.shield = 0.0               # Escudo actual
        self.shield_capacity = 0.0      # Capacidad máxima del escudo
        self.shield_regen_rate = 0.0    # Tasa de regeneración del escudo (% por segundo)
        self.shield_regen_delay = 5.0   # Tiempo sin recibir daño para regenerar (segundos)
        self.last_damage_time = 0       # Última vez que recibió daño
        self.damage_reflection = 0.0    # Porcentaje de daño reflejado

        # Cargar la imagen del héroe
        try:
            self.image = pygame.image.load("assets/heroe.png")
            self.image = pygame.transform.scale(self.image, (100, 100))
        except pygame.error as e:
            print(f"Error al cargar la imagen del héroe: {e}")
            self.image = None
            self.radius = 50
            self.color = (0, 0, 255)

        # Cargar las cuatro imágenes de las garras (tamaño aumentado al 150%)
        self.claws_images = []
        for i in range(4):
            try:
                if i == 0:
                    claws_image = pygame.image.load("assets/garras.png")
                else:
                    claws_image = pygame.image.load(f"assets/garras{i+1}.png")
                claws_image = pygame.transform.scale(claws_image, (150, 150))  # Tamaño aumentado de 100x100 a 150x150
                self.claws_images.append(claws_image)
            except pygame.error as e:
                print(f"Error al cargar la imagen garras{i+1 if i > 0 else ''}.png: {e}")
                claws_image = pygame.Surface((150, 150))  # Superficie de respaldo también ajustada
                claws_image.fill((255, 0, 0))  # Color rojo como respaldo
                self.claws_images.append(claws_image)

        # Variables para el efecto de las garras
        self.show_claws = False  # Controla si las garras deben mostrarse
        self.claws_timer = 0  # Temporizador para mostrar las garras
        self.claws_duration = 500  # Duración del efecto (0.5 segundos = 500 ms)
        self.current_claws_image = None  # Imagen de garras actual
        self.claws_alpha = 0  # Valor de opacidad para el desvanecimiento

    def draw(self, screen):
        self.update_recoil()
        # Dibujar al héroe
        if self.image:
            image_rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, image_rect)
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        # Dibujar las garras solo si show_claws es True
        if self.show_claws and self.current_claws_image:
            # Crear una copia de la imagen con opacidad
            claws_surface = self.current_claws_image.copy()
            claws_surface.set_alpha(int(self.claws_alpha))
            claws_rect = claws_surface.get_rect(center=(self.x, self.y))
            screen.blit(claws_surface, claws_rect)

            # Reducir el temporizador y actualizar la opacidad
            self.claws_timer -= 16  # Aproximadamente 16 ms por frame a 60 FPS
            elapsed_time = self.claws_duration - self.claws_timer
            self.claws_alpha = max(0, 255 - (255 * elapsed_time / self.claws_duration))
            if self.claws_timer <= 0:
                self.show_claws = False
                self.claws_timer = 0
                self.current_claws_image = None
                self.claws_alpha = 0

    def attack(self):
        # Permitir ataques con cada clic
        direction = random.choice([-1, 1])  # -1 (izquierda), 1 (derecha)
        return self.attack_power, direction

    def take_damage(self, damage):
        if damage > 0:  # Solo aplicar daño y activar las garras si el daño es mayor a 0
            # Reducir el daño con el escudo primero
            if self.shield > 0:
                if self.shield >= damage:
                    self.shield -= damage
                    damage = 0
                else:
                    damage -= self.shield
                    self.shield = 0

            # Aplicar el daño restante a la salud
            if damage > 0:
                self.health -= damage
                if self.health < 0:
                    self.health = 0
                self.last_damage_time = pygame.time.get_ticks() / 1000  # Tiempo en segundos

            # Activar el efecto de las garras
            self.show_claws = True
            self.claws_timer = self.claws_duration
            self.current_claws_image = random.choice(self.claws_images)  # Seleccionar una imagen aleatoria
            self.claws_alpha = 255  # Comenzar con opacidad completa

    def update_recoil(self):
        if self.recoil_timer > 0:
            # Moverse desde la posición base según la dirección
            if self.recoil_direction != 0:
                # Mover hacia izquierda o derecha
                self.x = self.base_x + (self.recoil_direction * self.recoil_speed * (self.recoil_duration - self.recoil_timer) / self.recoil_duration)
            else:
                # Mover hacia adelante (hacia arriba en la pantalla, eje y negativo)
                self.y = self.base_y - (self.recoil_speed * (self.recoil_duration - self.recoil_timer) / self.recoil_duration)

            self.recoil_timer -= 16
            if self.recoil_timer <= 0:
                # Regresar a la posición base
                self.x = self.base_x
                self.y = self.base_y
                self.recoil_direction = 0
        else:
            self.recoil_timer = 0
            self.x = self.base_x
            self.y = self.base_y

    def update_shield(self, dt):
        if self.shield_capacity <= 0 or self.shield_regen_rate <= 0:
            return

        current_time = pygame.time.get_ticks() / 1000  # Tiempo en segundos
        time_since_last_damage = current_time - self.last_damage_time

        if time_since_last_damage >= self.shield_regen_delay:
            # Regenerar el escudo
            regen_amount = self.shield_capacity * self.shield_regen_rate * dt
            self.shield = min(self.shield + regen_amount, self.shield_capacity)

    def reset_position(self):
        # Método para resetear la posición del héroe a su posición base
        self.x = self.base_x
        self.y = self.base_y
        self.recoil_timer = 0
        self.recoil_direction = 0
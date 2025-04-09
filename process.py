# process.py
import pygame

class Process:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.font = pygame.font.Font(None, 36)
        
        # Configuración de niveles
        self.current_level = 1
        self.enemies_defeated = 0
        self.enemies_per_level = 9  # Total de enemigos por nivel (3 puntitos x 3)
        self.enemies_per_dot = 3    # Cada puntito representa 3 enemigos
        
        # Configuración visual de los círculos y puntitos
        self.circle_y = 30
        self.circle_spacing = 70
        self.small_radius = 20
        self.large_radius = 28  # Aumentado de 25 a 28 para que el nivel actual sea más grande
        self.small_circle_radius = 4
        self.num_dots_per_level = 3  # Solo 3 puntitos entre niveles

        # Cargar la imagen process.png (más pequeña: 50x50)
        try:
            self.process_image = pygame.image.load("assets/process.png")
            self.process_image = pygame.transform.scale(self.process_image, (50, 50))  # Reducido de 70x70 a 50x50
        except pygame.error as e:
            print(f"Error al cargar process.png: {e}")
            self.process_image = pygame.Surface((50, 50))
            self.process_image.fill((255, 165, 0))  # Naranja como respaldo

        # Cargar background2.png (sin blur)
        try:
            self.background2 = pygame.image.load("assets/background2.png")
        except pygame.error as e:
            print(f"Error al cargar background2.png: {e}")
            self.background2 = pygame.Surface((self.screen_width, 100))
            self.background2.fill((50, 50, 50))

    def update(self):
        # Actualizar el nivel cuando se derrotan suficientes enemigos
        if self.enemies_defeated >= self.enemies_per_level:
            self.current_level += 1
            self.enemies_defeated = 0
            print(f"¡Subiste al nivel {self.current_level}!")
            return True  # Indica que se subió de nivel
        return False

    def enemy_defeated(self):
        # Incrementar el contador de enemigos derrotados
        self.enemies_defeated += 1

    def draw(self, screen, enemy_health, enemy_max_health):
        # Determinar qué niveles mostrar (siempre mostrar nivel anterior, actual y siguiente)
        levels_to_show = [self.current_level - 1, self.current_level, self.current_level + 1]
        if self.current_level == 1:
            levels_to_show = [1, 2]  # Solo mostrar 1 y 2 al inicio

        # Calcular posiciones de los círculos
        total_width = (len(levels_to_show) - 1) * self.circle_spacing
        start_x = (self.screen_width - total_width) // 2
        circle_positions = []

        # Dibujar los círculos de nivel con el fondo de background2.png
        for i, level in enumerate(levels_to_show):
            circle_x = start_x + i * self.circle_spacing
            circle_positions.append(circle_x)
            radius = self.large_radius if level == self.current_level else self.small_radius

            # Crear una superficie para el círculo
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            # Dibujar un círculo blanco como máscara
            pygame.draw.circle(circle_surface, (255, 255, 255), (radius, radius), radius)

            # Escalar la imagen background2.png para que quepa dentro del círculo
            scaled_background = pygame.transform.smoothscale(self.background2, (radius * 2, radius * 2))
            
            # Crear una superficie para el fondo
            background_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            # Centrar la imagen escalada en la superficie
            background_surface.blit(scaled_background, (0, 0))
            # Aplicar la máscara del círculo al fondo
            background_surface.blit(circle_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # Aplicar opacidad del 50% a los niveles pasado y futuro
            if level != self.current_level:
                background_surface.set_alpha(128)  # 50% de opacidad (128 de 255)
            else:
                background_surface.set_alpha(255)  # 100% de opacidad para el nivel actual

            # Dibujar el fondo dentro del círculo en la pantalla
            screen.blit(background_surface, (circle_x - radius, self.circle_y - radius))

            # Dibujar el borde interior (naranja para el nivel actual, gris para los demás)
            border_color = (255, 165, 0) if level == self.current_level else (150, 150, 150)
            border_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(border_surface, border_color, (radius, radius), radius, 2)
            # Aplicar opacidad al borde interior
            if level != self.current_level:
                border_surface.set_alpha(128)
            screen.blit(border_surface, (circle_x - radius, self.circle_y - radius))

            # Dibujar el borde blanco exterior (más grueso y uniforme)
            border_white_surface = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(border_white_surface, (255, 255, 255), (radius + 2, radius + 2), radius + 2, 4)
            # Aplicar opacidad al borde blanco
            if level != self.current_level:
                border_white_surface.set_alpha(128)
            screen.blit(border_white_surface, (circle_x - radius - 2, self.circle_y - radius - 2))

            # Dibujar el texto del nivel
            level_text_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            level_text = self.font.render(str(level), True, (255, 255, 255))
            level_text_rect = level_text.get_rect(center=(radius, radius))
            level_text_surface.blit(level_text, level_text_rect)
            # Aplicar opacidad al texto
            if level != self.current_level:
                level_text_surface.set_alpha(128)
            screen.blit(level_text_surface, (circle_x - radius, self.circle_y - radius))

        # Dibujar los puntitos entre los niveles (más separados)
        for i in range(len(circle_positions) - 1):
            start_circle_x = circle_positions[i]
            end_circle_x = circle_positions[i + 1]
            start_level = levels_to_show[i]
            # Ajustar el espacio para que los puntitos estén más separados
            space_between = end_circle_x - start_circle_x - (self.large_radius + self.small_radius)
            small_circle_spacing = space_between / (self.num_dots_per_level - 1) if self.num_dots_per_level > 1 else space_between  # Aumentar el espaciado

            # Calcular cuántos puntitos se han completado
            dots_completed = self.enemies_defeated // self.enemies_per_dot

            for j in range(self.num_dots_per_level):
                # Ajustar la posición para que los puntitos estén más separados
                small_circle_x = start_circle_x + self.large_radius + j * small_circle_spacing
                # Determinar el color del puntito
                if start_level < self.current_level:
                    # Entre nivel pasado y nivel actual: todos negros
                    dot_color = (0, 0, 0)
                elif start_level == self.current_level:
                    # Entre nivel actual y nivel futuro: pintar según enemigos derrotados
                    if j < dots_completed:
                        dot_color = (0, 0, 0)  # Negro para puntitos completados
                    else:
                        dot_color = (255, 255, 255)  # Blanco para puntitos pendientes
                else:
                    # Entre niveles futuros: todos blancos
                    dot_color = (255, 255, 255)

                # Crear una superficie para el puntito y aplicar opacidad si es necesario
                dot_surface = pygame.Surface((self.small_circle_radius * 2, self.small_circle_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(dot_surface, dot_color, (self.small_circle_radius, self.small_circle_radius), self.small_circle_radius)
                if start_level != self.current_level:
                    dot_surface.set_alpha(128)
                screen.blit(dot_surface, (int(small_circle_x) - self.small_circle_radius, self.circle_y - self.small_circle_radius))

        # Dibujar la imagen process.png en la parte superior derecha (más pequeña)
        process_x = self.screen_width - 70  # Ajustado para 50x50 (70 = 50 imagen + 20 margen)
        process_y = 10  # Un poco más abajo del borde superior
        screen.blit(self.process_image, (process_x, process_y))

        # Dibujar el texto de progreso debajo de la imagen (ajustado para el nuevo tamaño)
        progress_text = self.font.render(f"{self.enemies_defeated}/{self.enemies_per_level}", True, (255, 255, 255))
        progress_rect = progress_text.get_rect(center=(process_x + 25, process_y + 50 + 10))  # 25 = mitad de 50, +10 de margen
        screen.blit(progress_text, progress_rect)

        # Dibujar la barra de vida del enemigo en el centro del enemigo
        bar_width = 150  # Dimensiones de la barra grande
        bar_height = 16
        bar_x = (self.screen_width - bar_width) // 2  # Centrado en la pantalla
        bar_y = 70  # Posición del enemigo (ajustada para que esté en el centro del enemigo)
        health_ratio = enemy_health / enemy_max_health if enemy_max_health > 0 else 0
        filled_width = bar_width * health_ratio

        # Fondo de la barra (gris)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
        # Barra de salud (rojo)
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, filled_width, bar_height))
        # Borde de la barra
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 1)

    def get_current_level(self):
        return self.current_level
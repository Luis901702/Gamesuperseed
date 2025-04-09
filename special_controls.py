# special_controls.py
import pygame

class SpecialControls:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.special_attacks = game.special_attacks

        # Cargar imágenes para los círculos (ajustadas al nuevo tamaño)
        try:
            self.airdrop_icon = pygame.image.load("assets/airdrop.png")
            self.airdrop_icon = pygame.transform.scale(self.airdrop_icon, (42, 42))
        except pygame.error as e:
            print(f"Error al cargar airdrop.png para ícono: {e}")
            self.airdrop_icon = pygame.Surface((42, 42))
            self.airdrop_icon.fill((0, 255, 0))

        try:
            self.double_tap_icon = pygame.image.load("assets/double_tap.png")
            self.double_tap_icon = pygame.transform.scale(self.double_tap_icon, (42, 42))
        except pygame.error as e:
            print(f"Error al cargar double_tap.png para ícono: {e}")
            self.double_tap_icon = pygame.Surface((42, 42))
            self.double_tap_icon.fill((255, 255, 0))

        try:
            self.yieldstorm_icon = pygame.image.load("assets/yieldstorm.png")
            self.yieldstorm_icon = pygame.transform.scale(self.yieldstorm_icon, (42, 42))
        except pygame.error as e:
            print(f"Error al cargar yieldstorm.png para ícono: {e}")
            self.yieldstorm_icon = pygame.Surface((42, 42))
            self.yieldstorm_icon.fill((255, 0, 255))

        # Definir círculos base
        self.circle_base = [
            {"name": "Airdrop", "key": pygame.K_1, "icon": self.airdrop_icon},
            {"name": "Double Tap", "key": pygame.K_2, "icon": self.double_tap_icon},
            {"name": "Yieldstorm", "key": pygame.K_3, "icon": self.yieldstorm_icon}
        ]
        self.active_circles = []
        self.timer_font = pygame.font.Font(None, 24)  # Fuente para el contador

    def update_circles(self):
        """Actualiza los círculos activos según los ataques comprados."""
        self.active_circles = []
        x_start = 300
        for i, circle in enumerate(self.circle_base):
            attack = self.special_attacks.attacks[circle["name"]]
            if attack.purchased:
                self.active_circles.append({
                    "name": circle["name"],
                    "rect": pygame.Rect(x_start + (i * 70), 373, 54, 54),
                    "key": circle["key"],
                    "icon": circle["icon"]
                })

    def handle_events(self, event):
        self.update_circles()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for circle in self.active_circles:
                if circle["rect"].collidepoint(mouse_pos):
                    self.activate_special_attack(circle["name"])
        elif event.type == pygame.KEYDOWN:
            for circle in self.active_circles:
                if event.key == circle["key"]:
                    self.activate_special_attack(circle["name"])

    def activate_special_attack(self, name):
        attack = self.special_attacks.attacks[name]
        if attack.can_activate():
            damage, count = attack.activate()
            if name == "Airdrop":
                self.game.trigger_airdrop(count)
            elif name == "Double Tap":
                self.game.activate_double_tap()
            elif name == "Yieldstorm":
                print("Yieldstorm activado: las recompensas se multiplicarán por 2 durante 30 segundos")
            print(f"Ataque especial {name} activado")

    def draw(self):
        self.update_circles()
        current_time = pygame.time.get_ticks()
        for circle in self.active_circles:
            attack = self.special_attacks.attacks[circle["name"]]
            center = circle["rect"].center
            radius = circle["rect"].width // 2

            # Fondo negro
            pygame.draw.circle(self.screen, (0, 0, 0), center, radius)

            # Dibujar ícono
            icon_rect = circle["icon"].get_rect(center=center)
            self.screen.blit(circle["icon"], icon_rect)

            # Indicador de estado
            if attack.can_activate():
                pygame.draw.circle(self.screen, (0, 255, 0), center, radius, 4)
            else:
                remaining = max(0, attack.cooldown - current_time)
                progress = remaining / attack.cooldown_time
                pygame.draw.circle(self.screen, (50, 50, 50), center, radius, 4)
                if remaining > 0:
                    pygame.draw.arc(self.screen, (0, 255, 0), circle["rect"], -1.57, -1.57 + (2 * 3.14 * (1 - progress)), 4)

            # Contador de tiempo activo (solo para Double Tap y Yieldstorm)
            if attack.active and attack.duration is not None:
                elapsed = current_time - attack.active_start_time
                remaining_active = max(0, (attack.duration - elapsed) // 1000)
                timer_text = self.timer_font.render(str(remaining_active), True, (255, 255, 255))
                timer_rect = timer_text.get_rect(center=center)
                # Fondo circular negro más grande
                pygame.draw.circle(self.screen, (0, 0, 0), center, radius - 4)  # Abarca casi todo el círculo interno
                self.screen.blit(timer_text, timer_rect)

            # Borde blanco
            pygame.draw.circle(self.screen, (255, 255, 255), center, radius, 2)
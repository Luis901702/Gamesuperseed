import pygame
from allies import Ally
from heroe import Heroe

class GamingButton:
    def __init__(self, x, y, width, height, text, cost_text, color, hover_color, game):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.cost_text = cost_text
        self.color = color
        self.hover_color = hover_color
        self.game = game
        self.is_hovered = False
        self.is_pressed = False
        self.alpha = 100
        self.alpha_direction = 1
        
    def draw(self, surface):
        DARK_BLUE = (26, 31, 44)
        pygame.draw.rect(surface, DARK_BLUE, self.rect, border_radius=self.height//2)
        border_rect = self.rect.copy()
        pygame.draw.rect(surface, self.color if self.is_hovered else (self.color[0], self.color[1], self.color[2], 128), 
                        border_rect, 2, border_radius=self.height//2)
        if self.is_hovered:
            self.alpha += self.alpha_direction * 2
            if self.alpha >= 200 or self.alpha <= 100:
                self.alpha_direction *= -1
            glow_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            glow_color = (*self.color, self.alpha)
            pygame.draw.rect(glow_surface, glow_color, (5, 5, self.width, self.height), 
                            3, border_radius=self.height//2)
            surface.blit(glow_surface, (self.x - 5, self.y - 5))
        text_surface = self.game.button_font.render(self.text, True, (255, 255, 255))
        cost_font = pygame.font.Font(None, 16)
        cost_surface = cost_font.render(self.cost_text, True, (255, 255, 255))
        text_x = self.x + 10
        text_y = self.y + (self.height - text_surface.get_height()) // 2
        cost_x = self.x + self.width - cost_surface.get_width() - 10
        cost_y = self.y + (self.height - cost_surface.get_height()) // 2
        surface.blit(text_surface, (text_x, text_y))
        surface.blit(cost_surface, (cost_x, cost_y))

    def update(self, mouse_pos, mouse_pressed):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        if self.is_hovered and mouse_pressed[0] and not self.is_pressed:
            self.is_pressed = True
            print(f"Botón {self.text} clicado en {mouse_pos}")
            return True
        elif not mouse_pressed[0]:
            self.is_pressed = False
        return False

class UpgradeMenu:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.screen_width = game.screen_width
        self.screen_height = game.screen_height
        self.tab_font = pygame.font.Font(None, 24)
        self.game.button_font = pygame.font.Font(None, 20)

        self.DARK_BLUE = (26, 31, 44)
        self.DARKER_BLUE = (21, 26, 37)
        self.WHITE = (255, 255, 255)
        self.GREEN = (74, 222, 128)
        self.CYAN = (15, 160, 206)
        self.RED = (255, 0, 0)
        self.ORANGE = (255, 140, 0)
        self.BORDER_COLOR = (42, 48, 66)

        self.upgrade_scroll_offset = 0
        self.upgrade_scroll_speed = 180
        self.upgrade_menu_height = 110
        self.upgrade_menu_new_height = int(self.upgrade_menu_height * 1.5)
        self.menu_y = 426
        self.buttons_area_y = 471
        self.button_y_offset = 7

        self.scrollbar_rect = None
        self.is_dragging_scrollbar = False
        self.scrollbar_drag_start_y = 0
        self.max_scroll_offset = 0

        try:
            self.menu_background = pygame.image.load("assets/fondomenu.jpg").convert_alpha()
            self.menu_background = pygame.transform.scale(self.menu_background, (self.screen_width, self.upgrade_menu_new_height + 30))
            self.menu_background.set_alpha(204)
        except pygame.error as e:
            print(f"Error al cargar la imagen fondomenu.jpg: {e}")
            self.menu_background = None

        try:
            self.buttons_background = pygame.image.load("assets/fondomenu2.png").convert_alpha()
            self.buttons_background = pygame.transform.scale(self.buttons_background, (700, self.upgrade_menu_new_height))
        except pygame.error as e:
            print(f"Error al cargar la imagen fondomenu2.png: {e}")
            self.buttons_background = None

        self.buttons = []

        # Niveles y costos para Health (Shield Capacity y Shield Regen manejados aquí)
        self.max_health_level = 5
        self.shield_capacity_level = 0
        self.shield_regen_level = 0
        self.health_cost = 10  # Costo inicial para Increase Health
        self.shield_capacity_cost = 20  # Costo inicial para Shield Capacity
        self.shield_regen_cost = 15  # Costo inicial para Shield Regen

        # Niveles de mejora y costos para cada aliado
        self.max_upgrades = 5  # Máximo de mejoras por tipo
        # Seedfi
        self.seedfi_attack_level = 0
        self.seedfi_speed_level = 0
        self.seedfi_attack_cost = 5  # Costo inicial
        self.seedfi_speed_cost = 5  # Costo inicial
        # Bebop
        self.bebop_attack_level = 0
        self.bebop_speed_level = 0
        self.bebop_attack_cost = 10  # Costo inicial
        self.bebop_speed_cost = 10  # Costo inicial
        # Stryke
        self.stryke_attack_level = 0
        self.stryke_speed_level = 0
        self.stryke_attack_cost = 15
        self.stryke_speed_cost = 15
        # Velodrome
        self.velodrome_attack_level = 0
        self.velodrome_speed_level = 0
        self.velodrome_attack_cost = 20
        self.velodrome_speed_cost = 20
        # Ionic
        self.ionic_attack_level = 0
        self.ionic_speed_level = 0
        self.ionic_attack_cost = 25
        self.ionic_speed_cost = 25
        # BulletX
        self.bulletx_attack_level = 0
        self.bulletx_speed_level = 0
        self.bulletx_attack_cost = 30
        self.bulletx_speed_cost = 30
        # Mintpad
        self.mintpad_attack_level = 0
        self.mintpad_speed_level = 0
        self.mintpad_attack_cost = 35
        self.mintpad_speed_cost = 35
        # Fractal
        self.fractal_attack_level = 0
        self.fractal_speed_level = 0
        self.fractal_attack_cost = 40
        self.fractal_speed_cost = 40
        # Dolomite
        self.dolomite_attack_level = 0
        self.dolomite_speed_level = 0
        self.dolomite_attack_cost = 45
        self.dolomite_speed_cost = 45
        # Marginzero
        self.marginzero_attack_level = 0
        self.marginzero_speed_level = 0
        self.marginzero_attack_cost = 50
        self.marginzero_speed_cost = 50

        # Estadísticas de especiales
        self.airdrop_damage_level = 1
        self.airdrop_count_level = 1
        self.airdrop_damage_cost = 10
        self.airdrop_count_cost = 15
        self.double_tap_damage_level = 1
        self.double_tap_duration_level = 1
        self.double_tap_damage_cost = 10
        self.double_tap_duration_cost = 15
        self.yieldstorm_duration_level = 1
        self.yieldstorm_cooldown_level = 1
        self.yieldstorm_duration_cost = 10
        self.yieldstorm_cooldown_cost = 10

    def handle_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Clic detectado en {mouse_pos}")
            self.handle_tab_clicks(mouse_pos)
            if self.scrollbar_rect and self.scrollbar_rect.collidepoint(mouse_pos):
                self.is_dragging_scrollbar = True
                self.scrollbar_drag_start_y = mouse_pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging_scrollbar:
            delta_y = mouse_pos[1] - self.scrollbar_drag_start_y
            scroll_range = self.upgrade_menu_new_height - self.scrollbar_rect.height
            if scroll_range > 0:
                scroll_sensitivity = self.max_scroll_offset / scroll_range
                self.upgrade_scroll_offset -= delta_y * scroll_sensitivity
                self.upgrade_scroll_offset = min(0, max(self.upgrade_scroll_offset, -self.max_scroll_offset))
                self.scrollbar_drag_start_y = mouse_pos[1]

        elif event.type == pygame.MOUSEWHEEL:
            self.upgrade_scroll_offset += event.y * self.upgrade_scroll_speed
            self.upgrade_scroll_offset = min(0, max(self.upgrade_scroll_offset, -self.max_scroll_offset))
            print(f"Scroll offset después de rueda: {self.upgrade_scroll_offset}, Max scroll: {self.max_scroll_offset}")

        # Verificar cada botón
        for button in self.buttons:
            if button.update(mouse_pos, mouse_pressed):
                print(f"Procesando clic en botón: {button.text}")
                # Pestaña SPECIALS
                if self.game.active_tab == "specials":
                    print(f"SSC actual: {self.game.ssc}")
                    if button.text == "BUY AIRDROP" and self.game.ssc >= 50:
                        self.game.ssc -= 50
                        self.game.special_attacks.attacks["Airdrop"].purchase()
                        self.game.special_controls.update_circles()
                        self.game.show_tutorial("airdrop")
                        print(f"Airdrop comprado: SSC restante = {self.game.ssc}")
                    elif button.text == "BUY DOUBLE TAP" and self.game.ssc >= 50:
                        self.game.ssc -= 50
                        self.game.special_attacks.attacks["Double Tap"].purchase()
                        self.game.special_controls.update_circles()
                        self.game.show_tutorial("double_tap")
                        print(f"Double Tap comprado: SSC restante = {self.game.ssc}")
                    elif button.text == "BUY YIELDSTORM" and self.game.ssc >= 50:
                        self.game.ssc -= 50
                        self.game.special_attacks.attacks["Yieldstorm"].purchase()
                        self.game.special_controls.update_circles()
                        self.game.show_tutorial("yieldstorm")
                        print(f"Yieldstorm comprado: SSC restante = {self.game.ssc}")
                    elif button.text == "AIRDROP DAMAGE" and self.game.ssc >= self.airdrop_damage_cost and self.airdrop_damage_level < 6:
                        self.game.ssc -= self.airdrop_damage_cost
                        self.airdrop_damage_level += 1
                        self.game.special_attacks.attacks["Airdrop"].damage_level += 1
                        self.airdrop_damage_cost = int(self.airdrop_damage_cost * 1.5)
                        print(f"Mejorado daño de Airdrop al nivel {self.airdrop_damage_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "AIRDROP COUNT" and self.game.ssc >= self.airdrop_count_cost and self.airdrop_count_level < 5:
                        self.game.ssc -= self.airdrop_count_cost
                        self.airdrop_count_level += 1
                        self.game.special_attacks.attacks["Airdrop"].special_level += 1
                        self.airdrop_count_cost = int(self.airdrop_count_cost * 1.5)
                        print(f"Mejorada cantidad de Airdrop al nivel {self.airdrop_count_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "DOUBLE TAP DAMAGE" and self.game.ssc >= self.double_tap_damage_cost:
                        self.game.ssc -= self.double_tap_damage_cost
                        self.double_tap_damage_level += 1
                        self.game.special_attacks.attacks["Double Tap"].damage_level += 1
                        self.double_tap_damage_cost = int(self.double_tap_damage_cost * 1.5)
                        print(f"Mejorado daño de Double Tap al nivel {self.double_tap_damage_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "DOUBLE TAP DURATION" and self.game.ssc >= self.double_tap_duration_cost and self.double_tap_duration_level < 5:
                        self.game.ssc -= self.double_tap_duration_cost
                        self.double_tap_duration_level += 1
                        self.game.special_attacks.attacks["Double Tap"].special_level += 1
                        self.double_tap_duration_cost = int(self.double_tap_duration_cost * 1.5)
                        print(f"Mejorada duración de Double Tap al nivel {self.double_tap_duration_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "YIELDSTORM DURATION" and self.game.ssc >= self.yieldstorm_duration_cost and self.yieldstorm_duration_level < 5:
                        self.game.ssc -= self.yieldstorm_duration_cost
                        self.yieldstorm_duration_level += 1
                        self.game.special_attacks.attacks["Yieldstorm"].special_level += 1
                        self.yieldstorm_duration_cost = int(self.yieldstorm_duration_cost * 1.5)
                        print(f"Mejorada duración de Yieldstorm al nivel {self.yieldstorm_duration_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "YIELDSTORM COOLDOWN" and self.game.ssc >= self.yieldstorm_cooldown_cost and self.yieldstorm_cooldown_level < 5:
                        self.game.ssc -= self.yieldstorm_cooldown_cost
                        self.yieldstorm_cooldown_level += 1
                        self.game.special_attacks.attacks["Yieldstorm"].special_level += 1
                        self.yieldstorm_cooldown_cost = int(self.yieldstorm_cooldown_cost * 1.5)
                        print(f"Reducido cooldown de Yieldstorm al nivel {self.yieldstorm_cooldown_level}, SSC restantes: {self.game.ssc}")
                    else:
                        print(f"No se pudo procesar especial: SSC insuficiente ({self.game.ssc}/{self.airdrop_damage_cost}) o nivel máximo alcanzado")

                # Pestaña ALLIES
                elif self.game.active_tab == "allies":
                    print(f"SSC actual: {self.game.ssc}")
                    # Compra de aliados
                    if button.text == "SEEDFI" and not self.game.seedfi_purchased and self.game.ssc >= 50:
                        self.game.ssc -= 50
                        self.game.seedfi_purchased = True
                        self.game.allies.append(Ally(110, 310, ally_type="seedfi"))
                        print(f"Seedfi comprado y añadido en (110, 310), SSC restantes: {self.game.ssc}")
                    elif button.text == "BEBOP" and not self.game.bebop_purchased and self.game.ssc >= 80:
                        self.game.ssc -= 80
                        self.game.bebop_purchased = True
                        self.game.allies.append(Ally(180, 300, ally_type="bebop"))
                        print(f"Bebop comprado y añadido en (180, 300), SSC restantes: {self.game.ssc}")
                    elif button.text == "STRYKE" and not self.game.stryke_purchased and self.game.ssc >= 110:
                        self.game.ssc -= 110
                        self.game.stryke_purchased = True
                        self.game.allies.append(Ally(220, 315, ally_type="stryke"))
                        print(f"Stryke comprado y añadido en (220, 315), SSC restantes: {self.game.ssc}")
                    elif button.text == "VELODROME" and not self.game.velodrome_purchased and self.game.ssc >= 140:
                        self.game.ssc -= 140
                        self.game.velodrome_purchased = True
                        self.game.allies.append(Ally(560, 315, ally_type="velodrome"))
                        print(f"Velodrome comprado y añadido en (560, 315), SSC restantes: {self.game.ssc}")
                    elif button.text == "IONIC" and not self.game.ionic_purchased and self.game.ssc >= 170:
                        self.game.ssc -= 170
                        self.game.ionic_purchased = True
                        self.game.allies.append(Ally(620, 315, ally_type="ionic"))
                        print(f"Ionic comprado y añadido en (620, 315), SSC restantes: {self.game.ssc}")
                    elif button.text == "BULLETX" and not self.game.bulletx_purchased and self.game.ssc >= 200:
                        self.game.ssc -= 200
                        self.game.bulletx_purchased = True
                        self.game.allies.append(Ally(680, 315, ally_type="bulletx"))
                        print(f"BulletX comprado y añadido en (680, 315), SSC restantes: {self.game.ssc}")
                    elif button.text == "MINTPAD" and not self.game.mintpad_purchased and self.game.ssc >= 230:
                        self.game.ssc -= 230
                        self.game.mintpad_purchased = True
                        self.game.allies.append(Ally(60, 210, ally_type="mintpad"))
                        self.game.left_platform.set_visible(True)
                        print(f"Mintpad comprado y añadido en (60, 210), plataforma izquierda visible, SSC restantes: {self.game.ssc}")
                    elif button.text == "FRACTAL" and not self.game.fractal_purchased and self.game.ssc >= 260:
                        self.game.ssc -= 260
                        self.game.fractal_purchased = True
                        self.game.allies.append(Ally(140, 220, ally_type="fractal"))
                        self.game.left_platform.set_visible(True)
                        print(f"Fractal comprado y añadido en (140, 220), plataforma izquierda visible, SSC restantes: {self.game.ssc}")
                    elif button.text == "DOLOMITE" and not self.game.dolomite_purchased and self.game.ssc >= 290:
                        self.game.ssc -= 290
                        self.game.dolomite_purchased = True
                        self.game.allies.append(Ally(670, 210, ally_type="dolomite"))
                        self.game.right_platform.set_visible(True)
                        print(f"Dolomite comprado y añadido en (670, 210), plataforma derecha visible, SSC restantes: {self.game.ssc}")
                    elif button.text == "MARGINZERO" and not self.game.marginzero_purchased and self.game.ssc >= 320:
                        self.game.ssc -= 320
                        self.game.marginzero_purchased = True
                        self.game.allies.append(Ally(730, 220, ally_type="marginzero"))
                        self.game.right_platform.set_visible(True)
                        print(f"Marginzero comprado y añadido en (730, 220), plataforma derecha visible, SSC restantes: {self.game.ssc}")
                    # Mejoras de aliados
                    elif button.text == "SEEDFI ATTACK" and self.game.seedfi_purchased and self.game.ssc >= self.seedfi_attack_cost and self.seedfi_attack_level < self.max_upgrades:
                        self.game.ssc -= self.seedfi_attack_cost
                        self.seedfi_attack_level += 1
                        self.seedfi_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "seedfi":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Seedfi al nivel {self.seedfi_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "SEEDFI SPEED" and self.game.seedfi_purchased and self.game.ssc >= self.seedfi_speed_cost and self.seedfi_speed_level < self.max_upgrades:
                        self.game.ssc -= self.seedfi_speed_cost
                        self.seedfi_speed_level += 1
                        self.seedfi_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "seedfi":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Seedfi al nivel {self.seedfi_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "BEBOP ATTACK" and self.game.bebop_purchased and self.game.ssc >= self.bebop_attack_cost and self.bebop_attack_level < self.max_upgrades:
                        self.game.ssc -= self.bebop_attack_cost
                        self.bebop_attack_level += 1
                        self.bebop_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "bebop":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Bebop al nivel {self.bebop_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "BEBOP SPEED" and self.game.bebop_purchased and self.game.ssc >= self.bebop_speed_cost and self.bebop_speed_level < self.max_upgrades:
                        self.game.ssc -= self.bebop_speed_cost
                        self.bebop_speed_level += 1
                        self.bebop_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "bebop":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Bebop al nivel {self.bebop_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "STRYKE ATTACK" and self.game.stryke_purchased and self.game.ssc >= self.stryke_attack_cost and self.stryke_attack_level < self.max_upgrades:
                        self.game.ssc -= self.stryke_attack_cost
                        self.stryke_attack_level += 1
                        self.stryke_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "stryke":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Stryke al nivel {self.stryke_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "STRYKE SPEED" and self.game.stryke_purchased and self.game.ssc >= self.stryke_speed_cost and self.stryke_speed_level < self.max_upgrades:
                        self.game.ssc -= self.stryke_speed_cost
                        self.stryke_speed_level += 1
                        self.stryke_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "stryke":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Stryke al nivel {self.stryke_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "VELODROME ATTACK" and self.game.velodrome_purchased and self.game.ssc >= self.velodrome_attack_cost and self.velodrome_attack_level < self.max_upgrades:
                        self.game.ssc -= self.velodrome_attack_cost
                        self.velodrome_attack_level += 1
                        self.velodrome_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "velodrome":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Velodrome al nivel {self.velodrome_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "VELODROME SPEED" and self.game.velodrome_purchased and self.game.ssc >= self.velodrome_speed_cost and self.velodrome_speed_level < self.max_upgrades:
                        self.game.ssc -= self.velodrome_speed_cost
                        self.velodrome_speed_level += 1
                        self.velodrome_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "velodrome":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Velodrome al nivel {self.velodrome_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "IONIC ATTACK" and self.game.ionic_purchased and self.game.ssc >= self.ionic_attack_cost and self.ionic_attack_level < self.max_upgrades:
                        self.game.ssc -= self.ionic_attack_cost
                        self.ionic_attack_level += 1
                        self.ionic_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "ionic":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Ionic al nivel {self.ionic_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "IONIC SPEED" and self.game.ionic_purchased and self.game.ssc >= self.ionic_speed_cost and self.ionic_speed_level < self.max_upgrades:
                        self.game.ssc -= self.ionic_speed_cost
                        self.ionic_speed_level += 1
                        self.ionic_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "ionic":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Ionic al nivel {self.ionic_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "BULLETX ATTACK" and self.game.bulletx_purchased and self.game.ssc >= self.bulletx_attack_cost and self.bulletx_attack_level < self.max_upgrades:
                        self.game.ssc -= self.bulletx_attack_cost
                        self.bulletx_attack_level += 1
                        self.bulletx_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "bulletx":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de BulletX al nivel {self.bulletx_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "BULLETX SPEED" and self.game.bulletx_purchased and self.game.ssc >= self.bulletx_speed_cost and self.bulletx_speed_level < self.max_upgrades:
                        self.game.ssc -= self.bulletx_speed_cost
                        self.bulletx_speed_level += 1
                        self.bulletx_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "bulletx":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de BulletX al nivel {self.bulletx_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "MINTPAD ATTACK" and self.game.mintpad_purchased and self.game.ssc >= self.mintpad_attack_cost and self.mintpad_attack_level < self.max_upgrades:
                        self.game.ssc -= self.mintpad_attack_cost
                        self.mintpad_attack_level += 1
                        self.mintpad_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "mintpad":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Mintpad al nivel {self.mintpad_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "MINTPAD SPEED" and self.game.mintpad_purchased and self.game.ssc >= self.mintpad_speed_cost and self.mintpad_speed_level < self.max_upgrades:
                        self.game.ssc -= self.mintpad_speed_cost
                        self.mintpad_speed_level += 1
                        self.mintpad_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "mintpad":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Mintpad al nivel {self.mintpad_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "FRACTAL ATTACK" and self.game.fractal_purchased and self.game.ssc >= self.fractal_attack_cost and self.fractal_attack_level < self.max_upgrades:
                        self.game.ssc -= self.fractal_attack_cost
                        self.fractal_attack_level += 1
                        self.fractal_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "fractal":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Fractal al nivel {self.fractal_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "FRACTAL SPEED" and self.game.fractal_purchased and self.game.ssc >= self.fractal_speed_cost and self.fractal_speed_level < self.max_upgrades:
                        self.game.ssc -= self.fractal_speed_cost
                        self.fractal_speed_level += 1
                        self.fractal_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "fractal":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Fractal al nivel {self.fractal_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "DOLOMITE ATTACK" and self.game.dolomite_purchased and self.game.ssc >= self.dolomite_attack_cost and self.dolomite_attack_level < self.max_upgrades:
                        self.game.ssc -= self.dolomite_attack_cost
                        self.dolomite_attack_level += 1
                        self.dolomite_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "dolomite":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Dolomite al nivel {self.dolomite_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "DOLOMITE SPEED" and self.game.dolomite_purchased and self.game.ssc >= self.dolomite_speed_cost and self.dolomite_speed_level < self.max_upgrades:
                        self.game.ssc -= self.dolomite_speed_cost
                        self.dolomite_speed_level += 1
                        self.dolomite_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "dolomite":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Dolomite al nivel {self.dolomite_speed_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "MARGINZERO ATTACK" and self.game.marginzero_purchased and self.game.ssc >= self.marginzero_attack_cost and self.marginzero_attack_level < self.max_upgrades:
                        self.game.ssc -= self.marginzero_attack_cost
                        self.marginzero_attack_level += 1
                        self.marginzero_attack_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "marginzero":
                                ally.upgrade_attack_power()
                                print(f"Mejorado ataque de Marginzero al nivel {self.marginzero_attack_level}, SSC restantes: {self.game.ssc}")
                    elif button.text == "MARGINZERO SPEED" and self.game.marginzero_purchased and self.game.ssc >= self.marginzero_speed_cost and self.marginzero_speed_level < self.max_upgrades:
                        self.game.ssc -= self.marginzero_speed_cost
                        self.marginzero_speed_level += 1
                        self.marginzero_speed_cost += 1
                        for ally in self.game.allies:
                            if ally.ally_type == "marginzero":
                                ally.upgrade_attack_speed()
                                print(f"Mejorada velocidad de Marginzero al nivel {self.marginzero_speed_level}, SSC restantes: {self.game.ssc}")
                    else:
                        print(f"No se pudo procesar aliado: SSC insuficiente ({self.game.ssc}) o nivel máximo alcanzado")

                # Pestaña ATTACK
                elif self.game.active_tab == "attack":
                    print(f"Seeds actuales: {self.game.seeds_count}, Costo: {self.game.upgrades.attack_cost}")
                    if button.text == "INCREASE ATTACK" and self.game.seeds_count >= self.game.upgrades.attack_cost:
                        self.game.seeds_count -= self.game.upgrades.attack_cost
                        self.game.upgrades.apply_upgrade("attack", "Increase Attack")
                        print(f"Ataque del héroe aumentado a {self.game.heroe.attack_power}, Seeds restantes: {self.game.seeds_count}")
                    elif button.text == "CRITICAL HIT" and self.game.seeds_count >= self.game.upgrades.critical_hit_cost and self.game.upgrades.critical_hit_level < 5:
                        self.game.seeds_count -= self.game.upgrades.critical_hit_cost
                        self.game.upgrades.apply_upgrade("attack", "Critical Hit")
                        print(f"Golpe crítico mejorado a {self.game.heroe.critical_multiplier}, Seeds restantes: {self.game.seeds_count}")
                    elif button.text == "CRITICAL CHANCE" and self.game.seeds_count >= self.game.upgrades.critical_chance_cost and self.game.upgrades.critical_chance_level < 10:
                        self.game.seeds_count -= self.game.upgrades.critical_chance_cost
                        self.game.upgrades.apply_upgrade("attack", "Critical Chance")
                        print(f"Probabilidad de golpe crítico mejorada a {self.game.heroe.critical_chance*100}%, Seeds restantes: {self.game.seeds_count}")
                    else:
                        print(f"No se puede mejorar ataque: Seeds insuficientes ({self.game.seeds_count}/{self.game.upgrades.attack_cost}) o nivel máximo alcanzado")

                # Pestaña HEALTH
                elif self.game.active_tab == "health":
                    print(f"Seeds actuales: {self.game.seeds_count}")
                    if button.text == "INCREASE HEALTH" and self.game.seeds_count >= self.health_cost and self.game.upgrades.health_level < self.max_health_level:
                        self.game.seeds_count -= self.health_cost
                        self.game.upgrades.apply_upgrade("health", "Increase Health")
                        self.health_cost += 10
                        print(f"Salud del héroe aumentada a {self.game.heroe.max_health}, Seeds restantes: {self.game.seeds_count}")
                    elif button.text == "SHIELD CAPACITY" and self.game.seeds_count >= self.shield_capacity_cost and self.shield_capacity_level < self.max_health_level:
                        self.game.seeds_count -= self.shield_capacity_cost
                        self.shield_capacity_level += 1
                        self.game.heroe.shield_capacity += 20
                        self.game.heroe.shield = self.game.heroe.shield_capacity
                        self.shield_capacity_cost += 15
                        print(f"Capacidad de escudo aumentada a {self.game.heroe.shield_capacity}, Seeds restantes: {self.game.seeds_count}")
                    elif button.text == "SHIELD REGEN" and self.game.seeds_count >= self.shield_regen_cost and self.shield_regen_level < self.max_health_level:
                        self.game.seeds_count -= self.shield_regen_cost
                        self.shield_regen_level += 1
                        self.game.heroe.shield_regen_rate += 0.1
                        self.shield_regen_cost += 10
                        print(f"Regeneración de escudo aumentada a {self.game.heroe.shield_regen_rate}, Seeds restantes: {self.game.seeds_count}")
                    else:
                        print(f"No se puede realizar la mejora: Seeds insuficientes ({self.game.seeds_count}/{self.health_cost}) o nivel máximo alcanzado")

    def handle_tab_clicks(self, mouse_pos):
        if 50 <= mouse_pos[0] <= 200 and self.menu_y <= mouse_pos[1] <= self.menu_y + 30:
            self.game.active_tab = "health"
            print("Pestaña Health seleccionada")
        elif 233 <= mouse_pos[0] <= 383 and self.menu_y <= mouse_pos[1] <= self.menu_y + 30:
            self.game.active_tab = "attack"
            print("Pestaña Attack seleccionada")
        elif 417 <= mouse_pos[0] <= 567 and self.menu_y <= mouse_pos[1] <= self.menu_y + 30:
            self.game.active_tab = "specials"
            print("Pestaña Specials seleccionada")
        elif 600 <= mouse_pos[0] <= 750 and self.menu_y <= mouse_pos[1] <= self.menu_y + 30:
            self.game.active_tab = "allies"
            print("Pestaña Allies seleccionada")

    def draw(self):
        if self.menu_background:
            self.screen.blit(self.menu_background, (0, self.menu_y))
        else:
            pygame.draw.rect(self.screen, self.DARK_BLUE, (0, self.menu_y, self.screen_width, self.upgrade_menu_new_height + 30))
        pygame.draw.rect(self.screen, self.WHITE, (0, self.menu_y, self.screen_width, self.upgrade_menu_new_height + 30), 2)

        health_tab_color = self.CYAN if self.game.active_tab == "health" else self.DARKER_BLUE
        pygame.draw.rect(self.screen, health_tab_color, (50, self.menu_y, 150, 30), border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (50, self.menu_y, 150, 30), 2, border_top_left_radius=10, border_top_right_radius=10)
        health_text = self.tab_font.render("HEALTH", True, self.WHITE)
        self.screen.blit(health_text, health_text.get_rect(center=(125, self.menu_y + 15)))

        attack_tab_color = self.CYAN if self.game.active_tab == "attack" else self.DARKER_BLUE
        pygame.draw.rect(self.screen, attack_tab_color, (233, self.menu_y, 150, 30), border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (233, self.menu_y, 150, 30), 2, border_top_left_radius=10, border_top_right_radius=10)
        attack_text = self.tab_font.render("ATTACK", True, self.WHITE)
        self.screen.blit(attack_text, attack_text.get_rect(center=(308, self.menu_y + 15)))

        specials_tab_color = self.CYAN if self.game.active_tab == "specials" else self.DARKER_BLUE
        pygame.draw.rect(self.screen, specials_tab_color, (417, self.menu_y, 150, 30), border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (417, self.menu_y, 150, 30), 2, border_top_left_radius=10, border_top_right_radius=10)
        specials_text = self.tab_font.render("SPECIALS", True, self.WHITE)
        self.screen.blit(specials_text, specials_text.get_rect(center=(492, self.menu_y + 15)))

        allies_tab_color = self.CYAN if self.game.active_tab == "allies" else self.DARKER_BLUE
        pygame.draw.rect(self.screen, allies_tab_color, (600, self.menu_y, 150, 30), border_top_left_radius=10, border_top_right_radius=10)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, (600, self.menu_y, 150, 30), 2, border_top_left_radius=10, border_top_right_radius=10)
        allies_text = self.tab_font.render("ALLIES", True, self.WHITE)
        self.screen.blit(allies_text, allies_text.get_rect(center=(675, self.menu_y + 15)))

        if self.buttons_background:
            self.screen.blit(self.buttons_background, (50, self.buttons_area_y))
        else:
            pygame.draw.rect(self.screen, self.DARKER_BLUE, (50, self.buttons_area_y, 700, self.upgrade_menu_new_height))
        pygame.draw.rect(self.screen, self.CYAN, (50, self.buttons_area_y, 700, self.upgrade_menu_new_height), 2)

        clip_rect = pygame.Rect(50, self.buttons_area_y, 700, self.upgrade_menu_new_height)
        self.screen.set_clip(clip_rect)

        self.buttons = []
        total_content_height = 0

        # Pestaña HEALTH
        if self.game.active_tab == "health":
            y_offset = 0

            # Increase Health
            health_button = GamingButton(
                100, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                "INCREASE HEALTH" if self.game.upgrades.get_health_level() < self.max_health_level else "HEALTH MAXED",
                f"Lvl {self.game.upgrades.get_health_level()}/{self.max_health_level} - {self.health_cost} Seeds" if self.game.upgrades.get_health_level() < self.max_health_level else "Maxed",
                self.CYAN if self.game.upgrades.get_health_level() < self.max_health_level else self.GREEN,
                self.GREEN if self.game.upgrades.get_health_level() < self.max_health_level else self.CYAN,
                self.game
            )
            self.buttons.append(health_button)
            health_button.draw(self.screen)
            y_offset += 40

            # Shield Capacity
            shield_capacity_button = GamingButton(
                400, self.buttons_area_y + y_offset - 30 + self.upgrade_scroll_offset, 250, 30,
                "SHIELD CAPACITY" if self.shield_capacity_level < self.max_health_level else "CAPACITY MAXED",
                f"Lvl {self.shield_capacity_level}/{self.max_health_level} - {self.shield_capacity_cost} Seeds" if self.shield_capacity_level < self.max_health_level else "Maxed",
                self.CYAN if self.shield_capacity_level < self.max_health_level else self.GREEN,
                self.GREEN if self.shield_capacity_level < self.max_health_level else self.CYAN,
                self.game
            )
            self.buttons.append(shield_capacity_button)
            shield_capacity_button.draw(self.screen)
            y_offset += 40

            # Shield Regen
            shield_regen_button = GamingButton(
                100, self.buttons_area_y + y_offset - 30 + self.upgrade_scroll_offset, 250, 30,
                "SHIELD REGEN" if self.shield_regen_level < self.max_health_level else "REGEN MAXED",
                f"Lvl {self.shield_regen_level}/{self.max_health_level} - {self.shield_regen_cost} Seeds" if self.shield_regen_level < self.max_health_level else "Maxed",
                self.CYAN if self.shield_regen_level < self.max_health_level else self.GREEN,
                self.GREEN if self.shield_regen_level < self.max_health_level else self.CYAN,
                self.game
            )
            self.buttons.append(shield_regen_button)
            shield_regen_button.draw(self.screen)
            y_offset += 40

            total_content_height = y_offset
            self.max_scroll_offset = max(0, total_content_height - self.upgrade_menu_new_height)

        # Pestaña ATTACK
        elif self.game.active_tab == "attack":
            y_offset = 0

            # Increase Attack
            attack_button = GamingButton(
                100, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                "INCREASE ATTACK" if self.game.upgrades.get_attack_level() < 10 else "ATTACK MAXED",
                f"Lvl {self.game.upgrades.get_attack_level()}/10 - {self.game.upgrades.get_attack_cost()} Seeds" if self.game.upgrades.get_attack_level() < 10 else "Maxed",
                self.CYAN if self.game.upgrades.get_attack_level() < 10 else self.GREEN,
                self.GREEN if self.game.upgrades.get_attack_level() < 10 else self.CYAN,
                self.game
            )
            self.buttons.append(attack_button)
            attack_button.draw(self.screen)
            y_offset += 40

            # Critical Hit
            crit_hit_button = GamingButton(
                400, self.buttons_area_y + y_offset - 30 + self.upgrade_scroll_offset, 250, 30,
                "CRITICAL HIT" if self.game.upgrades.get_critical_hit_level() < 5 else "CRIT HIT MAXED",
                f"Lvl {self.game.upgrades.get_critical_hit_level()}/5 - {self.game.upgrades.get_critical_hit_cost()} Seeds" if self.game.upgrades.get_critical_hit_level() < 5 else "Maxed",
                self.CYAN if self.game.upgrades.get_critical_hit_level() < 5 else self.GREEN,
                self.GREEN if self.game.upgrades.get_critical_hit_level() < 5 else self.CYAN,
                self.game
            )
            self.buttons.append(crit_hit_button)
            crit_hit_button.draw(self.screen)
            y_offset += 40

            # Critical Chance
            crit_chance_button = GamingButton(
                100, self.buttons_area_y + y_offset - 30 + self.upgrade_scroll_offset, 250, 30,
                "CRITICAL CHANCE" if self.game.upgrades.get_critical_chance_level() < 10 else "CRIT CHANCE MAXED",
                f"Lvl {self.game.upgrades.get_critical_chance_level()}/10 - {self.game.upgrades.get_critical_chance_cost()} Seeds" if self.game.upgrades.get_critical_chance_level() < 10 else "Maxed",
                self.CYAN if self.game.upgrades.get_critical_chance_level() < 10 else self.GREEN,
                self.GREEN if self.game.upgrades.get_critical_chance_level() < 10 else self.CYAN,
                self.game
            )
            self.buttons.append(crit_chance_button)
            crit_chance_button.draw(self.screen)
            y_offset += 40

            total_content_height = y_offset
            self.max_scroll_offset = max(0, total_content_height - self.upgrade_menu_new_height)

        # Pestaña SPECIALS
        elif self.game.active_tab == "specials":
            y_offset = 0
            if self.game.special_attacks.attacks["Airdrop"].purchased:
                airdrop_title = self.tab_font.render("AIRDROP", True, (255, 255, 255))
                airdrop_title_rect = airdrop_title.get_rect(center=(self.screen_width // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                self.screen.blit(airdrop_title, airdrop_title_rect)
                airdrop_damage_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "AIRDROP DAMAGE" if self.airdrop_damage_level < 6 else "LEVEL MAX",
                    f"Lvl {self.airdrop_damage_level} - {self.airdrop_damage_cost} SSC" if self.airdrop_damage_level < 6 else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                airdrop_count_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "AIRDROP COUNT" if self.airdrop_count_level < 5 else "LEVEL MAX",
                    f"Lvl {self.airdrop_count_level} - {self.airdrop_count_cost} SSC" if self.airdrop_count_level < 5 else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(airdrop_damage_button)
                self.buttons.append(airdrop_count_button)
                airdrop_damage_button.draw(self.screen)
                airdrop_count_button.draw(self.screen)
                y_offset += 70
            else:
                buy_airdrop_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "BUY AIRDROP", "50 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(buy_airdrop_button)
                buy_airdrop_button.draw(self.screen)
                y_offset += 40

            if self.game.special_attacks.attacks["Double Tap"].purchased:
                double_tap_title = self.tab_font.render("DOUBLE TAP", True, (255, 255, 255))
                double_tap_title_rect = double_tap_title.get_rect(center=(self.screen_width // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                self.screen.blit(double_tap_title, double_tap_title_rect)
                double_tap_damage_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "DOUBLE TAP DAMAGE", f"Lvl {self.double_tap_damage_level} - {self.double_tap_damage_cost} SSC",
                    self.CYAN, self.CYAN, self.game
                )
                double_tap_duration_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "DOUBLE TAP DURATION" if self.double_tap_duration_level < 5 else "LEVEL MAX",
                    f"Lvl {self.double_tap_duration_level} - {self.double_tap_duration_cost} SSC" if self.double_tap_duration_level < 5 else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(double_tap_damage_button)
                self.buttons.append(double_tap_duration_button)
                double_tap_damage_button.draw(self.screen)
                double_tap_duration_button.draw(self.screen)
                y_offset += 70
            else:
                buy_double_tap_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "BUY DOUBLE TAP", "50 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(buy_double_tap_button)
                buy_double_tap_button.draw(self.screen)
                y_offset += 40

            if self.game.special_attacks.attacks["Yieldstorm"].purchased:
                yieldstorm_title = self.tab_font.render("YIELDSTORM", True, (255, 255, 255))
                yieldstorm_title_rect = yieldstorm_title.get_rect(center=(self.screen_width // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                self.screen.blit(yieldstorm_title, yieldstorm_title_rect)
                yieldstorm_duration_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "YIELDSTORM DURATION" if self.yieldstorm_duration_level < 5 else "LEVEL MAX",
                    f"Lvl {self.yieldstorm_duration_level} - {self.yieldstorm_duration_cost} SSC" if self.yieldstorm_duration_level < 5 else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                yieldstorm_cooldown_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "YIELDSTORM COOLDOWN" if self.yieldstorm_cooldown_level < 5 else "LEVEL MAX",
                    f"Lvl {self.yieldstorm_cooldown_level} - {self.yieldstorm_cooldown_cost} SSC" if self.yieldstorm_cooldown_level < 5 else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(yieldstorm_duration_button)
                self.buttons.append(yieldstorm_cooldown_button)
                yieldstorm_duration_button.draw(self.screen)
                yieldstorm_cooldown_button.draw(self.screen)
                y_offset += 70
            else:
                buy_yieldstorm_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "BUY YIELDSTORM", "50 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(buy_yieldstorm_button)
                buy_yieldstorm_button.draw(self.screen)
                y_offset += 40

            # Ajuste clave: Aumentar total_content_height para permitir más desplazamiento
            total_content_height = y_offset + 100  # Añadimos 100 píxeles extra para asegurar espacio
            self.max_scroll_offset = max(0, total_content_height - self.upgrade_menu_new_height)

        # Pestaña ALLIES
        elif self.game.active_tab == "allies":
            y_offset = 0
            total_content_height = 0

            if not self.game.seedfi_purchased:
                seedfi_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "SEEDFI", "50 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(seedfi_button)
                seedfi_button.draw(self.screen)
                y_offset += 40
            else:
                seedfi_title = self.tab_font.render("SEEDFI", True, (255, 255, 255))
                self.screen.blit(seedfi_title, (self.screen_width // 2 - seedfi_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                seedfi_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "SEEDFI ATTACK" if self.seedfi_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.seedfi_attack_level} - {self.seedfi_attack_cost} SSC" if self.seedfi_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                seedfi_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "SEEDFI SPEED" if self.seedfi_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.seedfi_speed_level} - {self.seedfi_speed_cost} SSC" if self.seedfi_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(seedfi_attack_button)
                self.buttons.append(seedfi_speed_button)
                seedfi_attack_button.draw(self.screen)
                seedfi_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.bebop_purchased:
                bebop_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "BEBOP", "80 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(bebop_button)
                bebop_button.draw(self.screen)
                y_offset += 40
            else:
                bebop_title = self.tab_font.render("BEBOP", True, (255, 255, 255))
                self.screen.blit(bebop_title, (self.screen_width // 2 - bebop_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                bebop_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "BEBOP ATTACK" if self.bebop_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.bebop_attack_level} - {self.bebop_attack_cost} SSC" if self.bebop_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                bebop_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "BEBOP SPEED" if self.bebop_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.bebop_speed_level} - {self.bebop_speed_cost} SSC" if self.bebop_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(bebop_attack_button)
                self.buttons.append(bebop_speed_button)
                bebop_attack_button.draw(self.screen)
                bebop_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.stryke_purchased:
                stryke_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "STRYKE", "110 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(stryke_button)
                stryke_button.draw(self.screen)
                y_offset += 40
            else:
                stryke_title = self.tab_font.render("STRYKE", True, (255, 255, 255))
                self.screen.blit(stryke_title, (self.screen_width // 2 - stryke_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                stryke_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "STRYKE ATTACK" if self.stryke_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.stryke_attack_level} - {self.stryke_attack_cost} SSC" if self.stryke_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                stryke_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "STRYKE SPEED" if self.stryke_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.stryke_speed_level} - {self.stryke_speed_cost} SSC" if self.stryke_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(stryke_attack_button)
                self.buttons.append(stryke_speed_button)
                stryke_attack_button.draw(self.screen)
                stryke_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.velodrome_purchased:
                velodrome_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "VELODROME", "140 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(velodrome_button)
                velodrome_button.draw(self.screen)
                y_offset += 40
            else:
                velodrome_title = self.tab_font.render("VELODROME", True, (255, 255, 255))
                self.screen.blit(velodrome_title, (self.screen_width // 2 - velodrome_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                velodrome_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "VELODROME ATTACK" if self.velodrome_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.velodrome_attack_level} - {self.velodrome_attack_cost} SSC" if self.velodrome_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                velodrome_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "VELODROME SPEED" if self.velodrome_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.velodrome_speed_level} - {self.velodrome_speed_cost} SSC" if self.velodrome_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(velodrome_attack_button)
                self.buttons.append(velodrome_speed_button)
                velodrome_attack_button.draw(self.screen)
                velodrome_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.ionic_purchased:
                ionic_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "IONIC", "170 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(ionic_button)
                ionic_button.draw(self.screen)
                y_offset += 40
            else:
                ionic_title = self.tab_font.render("IONIC", True, (255, 255, 255))
                self.screen.blit(ionic_title, (self.screen_width // 2 - ionic_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                ionic_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "IONIC ATTACK" if self.ionic_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.ionic_attack_level} - {self.ionic_attack_cost} SSC" if self.ionic_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                ionic_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "IONIC SPEED" if self.ionic_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.ionic_speed_level} - {self.ionic_speed_cost} SSC" if self.ionic_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(ionic_attack_button)
                self.buttons.append(ionic_speed_button)
                ionic_attack_button.draw(self.screen)
                ionic_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.bulletx_purchased:
                bulletx_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "BULLETX", "200 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(bulletx_button)
                bulletx_button.draw(self.screen)
                y_offset += 40
            else:
                bulletx_title = self.tab_font.render("BULLETX", True, (255, 255, 255))
                self.screen.blit(bulletx_title, (self.screen_width // 2 - bulletx_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                bulletx_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "BULLETX ATTACK" if self.bulletx_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.bulletx_attack_level} - {self.bulletx_attack_cost} SSC" if self.bulletx_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                bulletx_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "BULLETX SPEED" if self.bulletx_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.bulletx_speed_level} - {self.bulletx_speed_cost} SSC" if self.bulletx_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(bulletx_attack_button)
                self.buttons.append(bulletx_speed_button)
                bulletx_attack_button.draw(self.screen)
                bulletx_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.mintpad_purchased:
                mintpad_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "MINTPAD", "230 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(mintpad_button)
                mintpad_button.draw(self.screen)
                y_offset += 40
            else:
                mintpad_title = self.tab_font.render("MINTPAD", True, (255, 255, 255))
                self.screen.blit(mintpad_title, (self.screen_width // 2 - mintpad_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                mintpad_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "MINTPAD ATTACK" if self.mintpad_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.mintpad_attack_level} - {self.mintpad_attack_cost} SSC" if self.mintpad_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                mintpad_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "MINTPAD SPEED" if self.mintpad_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.mintpad_speed_level} - {self.mintpad_speed_cost} SSC" if self.mintpad_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(mintpad_attack_button)
                self.buttons.append(mintpad_speed_button)
                mintpad_attack_button.draw(self.screen)
                mintpad_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.fractal_purchased:
                fractal_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "FRACTAL", "260 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(fractal_button)
                fractal_button.draw(self.screen)
                y_offset += 40
            else:
                fractal_title = self.tab_font.render("FRACTAL", True, (255, 255, 255))
                self.screen.blit(fractal_title, (self.screen_width // 2 - fractal_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                fractal_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "FRACTAL ATTACK" if self.fractal_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.fractal_attack_level} - {self.fractal_attack_cost} SSC" if self.fractal_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                fractal_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "FRACTAL SPEED" if self.fractal_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.fractal_speed_level} - {self.fractal_speed_cost} SSC" if self.fractal_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(fractal_attack_button)
                self.buttons.append(fractal_speed_button)
                fractal_attack_button.draw(self.screen)
                fractal_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.dolomite_purchased:
                dolomite_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "DOLOMITE", "290 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(dolomite_button)
                dolomite_button.draw(self.screen)
                y_offset += 40
            else:
                dolomite_title = self.tab_font.render("DOLOMITE", True, (255, 255, 255))
                self.screen.blit(dolomite_title, (self.screen_width // 2 - dolomite_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                dolomite_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "DOLOMITE ATTACK" if self.dolomite_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.dolomite_attack_level} - {self.dolomite_attack_cost} SSC" if self.dolomite_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                dolomite_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "DOLOMITE SPEED" if self.dolomite_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.dolomite_speed_level} - {self.dolomite_speed_cost} SSC" if self.dolomite_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(dolomite_attack_button)
                self.buttons.append(dolomite_speed_button)
                dolomite_attack_button.draw(self.screen)
                dolomite_speed_button.draw(self.screen)
                y_offset += 70

            if not self.game.marginzero_purchased:
                marginzero_button = GamingButton(
                    275, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset, 250, 30,
                    "MARGINZERO", "320 SSC", self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(marginzero_button)
                marginzero_button.draw(self.screen)
                y_offset += 40
            else:
                marginzero_title = self.tab_font.render("MARGINZERO", True, (255, 255, 255))
                self.screen.blit(marginzero_title, (self.screen_width // 2 - marginzero_title.get_width() // 2, self.buttons_area_y + y_offset + 10 + self.upgrade_scroll_offset))
                marginzero_attack_button = GamingButton(
                    100, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "MARGINZERO ATTACK" if self.marginzero_attack_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.marginzero_attack_level} - {self.marginzero_attack_cost} SSC" if self.marginzero_attack_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                marginzero_speed_button = GamingButton(
                    400, self.buttons_area_y + y_offset + 35 + self.upgrade_scroll_offset, 250, 30,
                    "MARGINZERO SPEED" if self.marginzero_speed_level < self.max_upgrades else "LEVEL MAX",
                    f"Lvl {self.marginzero_speed_level} - {self.marginzero_speed_cost} SSC" if self.marginzero_speed_level < self.max_upgrades else "Maxed",
                    self.CYAN, self.CYAN, self.game
                )
                self.buttons.append(marginzero_attack_button)
                self.buttons.append(marginzero_speed_button)
                marginzero_attack_button.draw(self.screen)
                marginzero_speed_button.draw(self.screen)
                y_offset += 70

            total_content_height = y_offset + 80
            self.max_scroll_offset = max(0, total_content_height - self.upgrade_menu_new_height)

        self.screen.set_clip(None)

        if self.max_scroll_offset > 0:
            scrollbar_height = max(30, int(self.upgrade_menu_new_height * (self.upgrade_menu_new_height / total_content_height)))
            scroll_range = self.upgrade_menu_new_height - scrollbar_height - 20
            if scroll_range > 0:
                scrollbar_y = self.buttons_area_y + 10 + (scroll_range * (-self.upgrade_scroll_offset / self.max_scroll_offset))
                scrollbar_y = max(self.buttons_area_y + 10, min(scrollbar_y, self.buttons_area_y + self.upgrade_menu_new_height - 20 - scrollbar_height))
                self.scrollbar_rect = pygame.Rect(740, scrollbar_y, 10, scrollbar_height)

                pygame.draw.rect(self.screen, (50, 50, 50), (740, self.buttons_area_y, 10, self.upgrade_menu_new_height - 10))
                pygame.draw.rect(self.screen, (100, 100, 100), self.scrollbar_rect)
                pygame.draw.rect(self.screen, self.CYAN, self.scrollbar_rect, 1)

                arrow_up_points = [
                    (745, self.buttons_area_y),
                    (740, self.buttons_area_y + 10),
                    (750, self.buttons_area_y + 10)
                ]
                pygame.draw.polygon(self.screen, self.CYAN, arrow_up_points)
                pygame.draw.polygon(self.screen, (100, 100, 100), arrow_up_points, 1)

                arrow_down_points = [
                    (745, self.buttons_area_y + self.upgrade_menu_new_height - 10),
                    (740, self.buttons_area_y + self.upgrade_menu_new_height - 20),
                    (750, self.buttons_area_y + self.upgrade_menu_new_height - 20)
                ]
                pygame.draw.polygon(self.screen, self.CYAN, arrow_down_points)
                pygame.draw.polygon(self.screen, (100, 100, 100), arrow_down_points, 1)
            else:
                self.scrollbar_rect = None
        else:
            self.scrollbar_rect = None
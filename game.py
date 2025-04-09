import pygame
import random
import time

from heroe import Heroe
from enemy import Enemy
from allies import Ally
from upgrades import Upgrades
from seed import Seed
from process import Process
from bullet import Bullet
from upgrade_menu import UpgradeMenu
from special_attacks import SpecialAttacks
from anuncio import Anuncio
from special_controls import SpecialControls
from platforms import Platform
from sounds import SoundManager  # Importar SoundManager

class Game:
    def __init__(self):
        self.instance_id = id(self)
        print(f"Nueva instancia de Game creada con ID: {self.instance_id}")

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.damage_font = pygame.font.Font(None, 30)
        self.word_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 28)

        # Inicializar SoundManager y comenzar la música de fondo
        self.sound_manager = SoundManager()
        self.sound_manager.play_background_music()  # Iniciar la música aquí

        # Cargar fondos
        try:
            self.background2 = pygame.image.load("assets/background2.png")
            self.background2 = pygame.transform.scale(self.background2, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error al cargar el fondo secundario (background2): {e}")
            self.background2 = None

        try:
            self.background = pygame.image.load("assets/background.png")
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error al cargar el fondo principal (background): {e}")
            self.background = None

        try:
            self.darkbackground2 = pygame.image.load("assets/darkbackground2.png")
            self.darkbackground2 = pygame.transform.scale(self.darkbackground2, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error al cargar el fondo oscuro secundario (darkbackground2): {e}")
            self.darkbackground2 = None

        try:
            self.darkbackground = pygame.image.load("assets/darkbackground.png")
            self.darkbackground = pygame.transform.scale(self.darkbackground, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Error al cargar el fondo oscuro principal (darkbackground): {e}")
            self.darkbackground = None

        # Cargar imágenes de flash
        self.flash_images = []
        for i in range(1, 5):
            try:
                flash_image = pygame.image.load(f"assets/flashattack{i}.png")
                flash_image = pygame.transform.scale(flash_image, (200, 200))
                self.flash_images.append(flash_image)
            except pygame.error as e:
                print(f"Error al cargar la imagen flashattack{i}.png: {e}")

        # Cargar imágenes de bossback
        self.bossback_images = []
        for i in ["bossback", "bossback2", "bossback3"]:
            try:
                bossback_image = pygame.image.load(f"assets/{i}.png")
                original_size = bossback_image.get_size()
                new_size = (int(original_size[0] * 1.4), int(original_size[1] * 1.4))
                bossback_image = pygame.transform.scale(bossback_image, new_size)
                self.bossback_images.append(bossback_image)
            except pygame.error as e:
                print(f"Error al cargar {i}.png: {e}")
                self.bossback_images.append(pygame.Surface((200, 200)))

        # Cargar íconos de aliados
        try:
            self.seedfi_icon = pygame.image.load("assets/seedfi.png")
            self.seedfi_icon = pygame.transform.scale(self.seedfi_icon, (20, 20))
        except pygame.error as e:
            self.seedfi_icon = pygame.Surface((20, 20))
            self.seedfi_icon.fill((34, 139, 34))

        try:
            self.bebop_icon = pygame.image.load("assets/bebop.png")
            self.bebop_icon = pygame.transform.scale(self.bebop_icon, (20, 20))
        except pygame.error as e:
            self.bebop_icon = pygame.Surface((20, 20))
            self.bebop_icon.fill((0, 102, 204))

        try:
            self.stryke_icon = pygame.image.load("assets/stryke.png")
            self.stryke_icon = pygame.transform.scale(self.stryke_icon, (20, 20))
        except pygame.error as e:
            self.stryke_icon = pygame.Surface((20, 20))
            self.stryke_icon.fill((255, 215, 0))

        try:
            self.velodrome_icon = pygame.image.load("assets/velodrome.png")
            self.velodrome_icon = pygame.transform.scale(self.velodrome_icon, (20, 20))
        except pygame.error as e:
            self.velodrome_icon = pygame.Surface((20, 20))
            self.velodrome_icon.fill((128, 0, 128))

        try:
            self.ionic_icon = pygame.image.load("assets/ionic.png")
            self.ionic_icon = pygame.transform.scale(self.ionic_icon, (20, 20))
        except pygame.error as e:
            print(f"Error al cargar ionic.png: {e}")
            self.ionic_icon = pygame.Surface((20, 20))
            self.ionic_icon.fill((0, 255, 255))

        try:
            self.bulletx_icon = pygame.image.load("assets/bulletx.png")
            self.bulletx_icon = pygame.transform.scale(self.bulletx_icon, (20, 20))
        except pygame.error as e:
            print(f"Error al cargar bulletx.png: {e}")
            self.bulletx_icon = pygame.Surface((20, 20))
            self.bulletx_icon.fill((255, 0, 0))

        # Cargar imágenes de recursos
        try:
            self.seeds_image = pygame.image.load("assets/seeds.png")
            self.seeds_image = pygame.transform.scale(self.seeds_image, (30, 30))
        except pygame.error as e:
            self.seeds_image = pygame.Surface((30, 30))
            self.seeds_image.fill((255, 255, 0))

        try:
            self.ssc_image = pygame.image.load("assets/SSC.png")
            self.ssc_image = pygame.transform.scale(self.ssc_image, (30, 30))
        except pygame.error as e:
            self.ssc_image = pygame.Surface((30, 30))
            self.ssc_image.fill((0, 255, 255))

        # Cargar imagen de Airdrop
        try:
            self.airdrop_image = pygame.image.load("assets/airdrop.png")
            self.airdrop_image = pygame.transform.scale(self.airdrop_image, (130, 130))
        except pygame.error as e:
            print(f"Error al cargar airdrop.png: {e}")
            self.airdrop_image = pygame.Surface((130, 130))
            self.airdrop_image.fill((0, 255, 0))

        # Cargar imagen de explosión de Airdrop
        try:
            self.explosion_image = pygame.image.load("assets/explosionairdrop.png")
            self.explosion_image = pygame.transform.scale(self.explosion_image, (130, 130))
        except pygame.error as e:
            print(f"Error al cargar explosionairdrop.png: {e}")
            self.explosion_image = pygame.Surface((130, 130))
            self.explosion_image.fill((255, 0, 0))

        # Inicializar objetos principales
        self.heroe = Heroe(self.screen_width // 2, self.screen_height // 2 + 50)
        self.enemy = Enemy(self.screen_width // 2, 200, level=self.process.get_current_level() if hasattr(self, 'process') else 1)

        self.left_platform = Platform(100, 270, side="left")
        self.right_platform = Platform(700, 270, side="right")

        self.mintpad_purchased = False
        self.fractal_purchased = False
        self.dolomite_purchased = False
        self.marginzero_purchased = False

        self.allies = []
        self.seedfi_purchased = False
        self.bebop_purchased = False
        self.stryke_purchased = False
        self.velodrome_purchased = False
        self.ionic_purchased = False
        self.bulletx_purchased = False

        self.bullets = []
        self.seeds = []
        self.upgrades = Upgrades(self.heroe, self.allies)
        self.special_attacks = SpecialAttacks(self.heroe)
        self.seeds_count = 0
        self.ssc = 0

        self.process = Process(self.screen_width)

        self.active_tab = "health"
        self.flash_alpha = 0
        self.flash_duration = 200
        self.flash_start_time = 0
        self.current_flash_image = None
        self.flash_offset_x = 0
        self.flash_offset_y = 0

        self.current_bossback = None
        self.bossback_timer = 0
        self.bossback_duration = 400
        self.bossback_interval = random.randint(1500, 3000)

        self.damage_texts = []
        self.word_texts = []
        self.words = ["supergm", "defi", "defi is freedom", "superseed", "superchain", "burn debt"]
        self.attack_counter = 0
        self.next_word_attack = random.randint(4, 10)

        self.running = True
        self.game_over = False
        self.paused = False

        self.pause_button_rect = pygame.Rect(self.screen_width - 120, 10, 40, 40)
        self.pause_button_color = (255, 165, 0)
        self.pause_button_border_color = (200, 100, 0)
        self.pause_button_text = pygame.font.Font(None, 20).render("||", True, (255, 255, 255))

        self.pause_menu_rect = pygame.Rect(self.screen_width // 2 - 150, self.screen_height // 2 - 90, 300, 180)
        self.pause_menu_background = pygame.Surface((300, 180), pygame.SRCALPHA)
        for y in range(180):
            r = 10 + (20 - 10) * (y / 180)
            g = 10 + (50 - 10) * (y / 180)
            b = 10 + (138 - 10) * (y / 180)
            pygame.draw.line(self.pause_menu_background, (int(r), int(g), int(b)), (0, y), (300, y))
        
        self.resume_button_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2 - 20, 120, 40)
        self.exit_button_rect = pygame.Rect(self.screen_width // 2 - 60, self.screen_height // 2 + 30, 120, 40)
        self.button_base_color = (30, 27, 75)
        self.button_mid_color = (30, 58, 138)
        self.button_text_color = (165, 243, 252)
        
        self.pause_close_rect = pygame.Rect(self.screen_width // 2 + 115, self.screen_height // 2 - 80, 30, 30)
        self.pause_close_color = (100, 100, 100)
        self.pause_close_hover = False

        self.upgrade_menu = UpgradeMenu(self)
        self.anuncio = Anuncio(self.screen_width, self.screen_height)
        self.tutorial_active = False

        self.special_controls = SpecialControls(self)
        self.airdrop_particles = []
        self.explosion_particles = []

        self.double_tap_active = False
        self.double_tap_start_time = 0
        self.double_tap_particles = []

    def activate_double_tap(self):
        if not self.double_tap_active:
            self.double_tap_active = True
            self.double_tap_start_time = pygame.time.get_ticks()
            self.heroe.attack_power *= 2
            print(f"Double Tap activado: ataque del héroe aumentado a {self.heroe.attack_power}")

    def show_tutorial(self, attack_name):
        print(f"Activando tutorial para {attack_name}")
        self.tutorial_active = True
        self.anuncio.active = True
        self.anuncio.load_image(attack_name)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.tutorial_active:
                    if self.anuncio.handle_events(event):
                        print("Tutorial cerrado")
                        self.tutorial_active = False
                        self.anuncio.active = False
                elif self.paused:
                    result = self.handle_pause_events(event)
                    if result == "resume" or result == "close":
                        self.paused = False
                    elif result == "exit":
                        self.running = False
                elif self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.restart_game()
                else:
                    self.handle_events(event)

            if not hasattr(self, 'frozen_screen') or self.frozen_screen is None:
                self.frozen_screen = self.screen.copy()

            if self.tutorial_active:
                self.draw_tutorial()
            elif self.paused:
                self.draw_pause()
            elif self.game_over:
                self.draw_game_over()
            else:
                self.update(dt)
                self.draw()
                self.frozen_screen = None

        # Detener la música cuando el juego termina
        self.sound_manager.stop_background_music()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Ataque con tecla Espacio detectado")
                self.perform_attack()
                return
            elif event.key == pygame.K_p:
                self.paused = not self.paused

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Clic detectado en: {mouse_pos}")
            if self.pause_button_rect.collidepoint(mouse_pos):
                self.paused = True
            elif mouse_pos[1] < self.screen_height - 150:
                self.perform_attack()

        self.upgrade_menu.handle_events(event)
        self.special_controls.handle_events(event)

    def handle_pause_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.resume_button_rect.collidepoint(mouse_pos):
                return "resume"
            elif self.exit_button_rect.collidepoint(mouse_pos):
                return "exit"
            elif self.pause_close_rect.collidepoint(mouse_pos):
                return "close"
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.pause_close_hover = self.pause_close_rect.collidepoint(mouse_pos)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                return "resume"
        
        return None

    def draw_mystery_button(self, rect, text, hovered):
        pygame.draw.rect(self.screen, self.button_base_color, rect, border_radius=15)
        pygame.draw.rect(self.screen, self.button_mid_color, rect, 2, border_radius=15)
        text_surface = self.button_font.render(text, True, self.button_text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        if hovered:
            line_y = rect.y + rect.height - 5
            pygame.draw.line(self.screen, self.button_text_color, (rect.x + 10, line_y), 
                            (rect.x + rect.width - 10, line_y), 2)

    def draw_pause(self):
        if self.frozen_screen:
            self.screen.blit(self.frozen_screen, (0, 0))
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(self.pause_menu_background, self.pause_menu_rect)
        pygame.draw.rect(self.screen, (70, 130, 180, 128), self.pause_menu_rect, 3, border_radius=15)
        mouse_pos = pygame.mouse.get_pos()
        resume_hovered = self.resume_button_rect.collidepoint(mouse_pos)
        exit_hovered = self.exit_button_rect.collidepoint(mouse_pos)
        self.draw_mystery_button(self.resume_button_rect, "Resume", resume_hovered)
        self.draw_mystery_button(self.exit_button_rect, "Exit", exit_hovered)
        pygame.draw.rect(self.screen, self.pause_close_color if not self.pause_close_hover else (150, 150, 150), 
                         self.pause_close_rect, border_radius=5)
        close_text = self.font.render("X", True, (255, 255, 255))
        close_text_rect = close_text.get_rect(center=self.pause_close_rect.center)
        self.screen.blit(close_text, close_text_rect)
        pygame.display.flip()

    def draw_tutorial(self):
        print("Dibujando tutorial")
        if self.frozen_screen:
            self.screen.blit(self.frozen_screen, (0, 0))
        self.anuncio.draw(self.screen)
        pygame.display.flip()

    def perform_attack(self):
        print("Ejecutando perform_attack")
        damage, direction = self.heroe.attack()
        if random.random() < self.heroe.critical_chance:
            print("¡Ataque crítico!")
            damage *= self.heroe.critical_multiplier
        print(f"Aplicando {damage} de daño al enemigo")
        self.enemy.take_damage(damage)
        self.add_damage_text(damage)
        self.sound_manager.play_random_hero_attack()  # Reproducir sonido aleatorio de ataque del héroe

        self.attack_counter += 1
        if self.attack_counter >= self.next_word_attack:
            self.add_word_text()
            self.attack_counter = 0
            self.next_word_attack = random.randint(4, 10)

        self.heroe.recoil_direction = direction if random.random() < 0.5 else 0
        self.heroe.recoil_timer = self.heroe.recoil_duration
        self.flash_alpha = 255
        self.flash_start_time = pygame.time.get_ticks()
        if self.flash_images:
            self.current_flash_image = random.choice(self.flash_images)
            print("Partículas flashattack activadas")
        self.flash_offset_x = random.randint(-20, 20)
        self.flash_offset_y = random.randint(-20, 20)

        if self.double_tap_active and random.random() < 0.5:
            self.double_tap_particles.append({
                "x": self.heroe.x + random.randint(-20, 20),
                "y": self.heroe.y - 20,
                "life": 1000
            })

    def add_damage_text(self, damage):
        text = self.damage_font.render(f"-{damage:.2f}", True, (255, 0, 0))
        x = self.enemy.x + random.randint(-50, 50)
        y = self.enemy.y + random.randint(-50, 50)
        self.damage_texts.append({"text": text, "x": x, "y": y, "life": 200})

    def add_word_text(self):
        word = random.choice(self.words)
        text = self.word_font.render(word, True, (0, 255, 0))
        x = self.enemy.x + random.randint(-50, 50)
        y = self.enemy.y + random.randint(-50, 50)
        self.word_texts.append({"text": text, "x": x, "y": y, "life": 200})

    def restart_game(self):
        print(f"Reiniciando juego. Aliados antes de reiniciar: {len(self.allies)}")
        special_attacks_state = {}
        for name, attack in self.special_attacks.attacks.items():
            special_attacks_state[name] = {
                "purchased": attack.purchased,
                "damage_level": attack.damage_level,
                "damage_cost": attack.damage_cost,
                "special_level": attack.special_level,
                "special_cost": attack.special_cost,
                "cooldown_time": attack.cooldown_time,
                "duration": attack.duration,
                "active": attack.active,
                "active_start_time": attack.active_start_time
            }
        saved_allies = []
        for ally in self.allies:
            saved_allies.append({
                "ally_type": ally.ally_type,
                "x": ally.x,
                "y": ally.y,
                "attack_power": ally.attack_power,
                "attack_speed": ally.attack_speed,
                "attack_interval": ally.attack_interval
            })
        saved_purchases = {
            "seedfi_purchased": self.seedfi_purchased,
            "bebop_purchased": self.bebop_purchased,
            "stryke_purchased": self.stryke_purchased,
            "velodrome_purchased": self.velodrome_purchased,
            "ionic_purchased": self.ionic_purchased,
            "bulletx_purchased": self.bulletx_purchased,
            "mintpad_purchased": self.mintpad_purchased,
            "fractal_purchased": self.fractal_purchased,
            "dolomite_purchased": self.dolomite_purchased,
            "marginzero_purchased": self.marginzero_purchased
        }
        upgrades_state = {
            "attack_level": self.upgrades.attack_level,
            "attack_cost": self.upgrades.attack_cost,
            "critical_hit_level": self.upgrades.critical_hit_level,
            "critical_hit_cost": self.upgrades.critical_hit_cost,
            "critical_chance_level": self.upgrades.critical_chance_level,
            "critical_chance_cost": self.upgrades.critical_chance_cost,
            "health_level": self.upgrades.health_level,
            "health_cost": self.upgrades.health_cost
        }
        heroe_state = {
            "attack_power": self.heroe.attack_power,
            "attack_speed": self.heroe.attack_speed,
            "max_health": self.heroe.max_health,
            "critical_chance": self.heroe.critical_chance,
            "critical_multiplier": self.heroe.critical_multiplier,
            "shield_capacity": self.heroe.shield_capacity,
            "shield_regen_rate": self.heroe.shield_regen_rate
        }
        upgrade_menu_state = {
            "airdrop_damage_level": self.upgrade_menu.airdrop_damage_level,
            "airdrop_damage_cost": self.upgrade_menu.airdrop_damage_cost,
            "airdrop_count_level": self.upgrade_menu.airdrop_count_level,
            "airdrop_count_cost": self.upgrade_menu.airdrop_count_cost,
            "double_tap_damage_level": self.upgrade_menu.double_tap_damage_level,
            "double_tap_damage_cost": self.upgrade_menu.double_tap_damage_cost,
            "double_tap_duration_level": self.upgrade_menu.double_tap_duration_level,
            "double_tap_duration_cost": self.upgrade_menu.double_tap_duration_cost,
            "yieldstorm_duration_level": self.upgrade_menu.yieldstorm_duration_level,
            "yieldstorm_duration_cost": self.upgrade_menu.yieldstorm_duration_cost,
            "yieldstorm_cooldown_level": self.upgrade_menu.yieldstorm_cooldown_level,
            "yieldstorm_cooldown_cost": self.upgrade_menu.yieldstorm_cooldown_cost,
            "seedfi_attack_level": self.upgrade_menu.seedfi_attack_level,
            "seedfi_attack_cost": self.upgrade_menu.seedfi_attack_cost,
            "seedfi_speed_level": self.upgrade_menu.seedfi_speed_level,
            "seedfi_speed_cost": self.upgrade_menu.seedfi_speed_cost,
            "bebop_attack_level": self.upgrade_menu.bebop_attack_level,
            "bebop_attack_cost": self.upgrade_menu.bebop_attack_cost,
            "bebop_speed_level": self.upgrade_menu.bebop_speed_level,
            "bebop_speed_cost": self.upgrade_menu.bebop_speed_cost,
            "stryke_attack_level": self.upgrade_menu.stryke_attack_level,
            "stryke_attack_cost": self.upgrade_menu.stryke_attack_cost,
            "stryke_speed_level": self.upgrade_menu.stryke_speed_level,
            "stryke_speed_cost": self.upgrade_menu.stryke_speed_cost,
            "velodrome_attack_level": self.upgrade_menu.velodrome_attack_level,
            "velodrome_attack_cost": self.upgrade_menu.velodrome_attack_cost,
            "velodrome_speed_level": self.upgrade_menu.velodrome_speed_level,
            "velodrome_speed_cost": self.upgrade_menu.velodrome_speed_cost,
            "ionic_attack_level": self.upgrade_menu.ionic_attack_level,
            "ionic_attack_cost": self.upgrade_menu.ionic_attack_cost,
            "ionic_speed_level": self.upgrade_menu.ionic_speed_level,
            "ionic_speed_cost": self.upgrade_menu.ionic_speed_cost,
            "bulletx_attack_level": self.upgrade_menu.bulletx_attack_level,
            "bulletx_attack_cost": self.upgrade_menu.bulletx_attack_cost,
            "bulletx_speed_level": self.upgrade_menu.bulletx_speed_level,
            "bulletx_speed_cost": self.upgrade_menu.bulletx_speed_cost,
            "mintpad_attack_level": self.upgrade_menu.mintpad_attack_level,
            "mintpad_attack_cost": self.upgrade_menu.mintpad_attack_cost,
            "mintpad_speed_level": self.upgrade_menu.mintpad_speed_level,
            "mintpad_speed_cost": self.upgrade_menu.mintpad_speed_cost,
            "fractal_attack_level": self.upgrade_menu.fractal_attack_level,
            "fractal_attack_cost": self.upgrade_menu.fractal_attack_cost,
            "fractal_speed_level": self.upgrade_menu.fractal_speed_level,
            "fractal_speed_cost": self.upgrade_menu.fractal_speed_cost,
            "dolomite_attack_level": self.upgrade_menu.dolomite_attack_level,
            "dolomite_attack_cost": self.upgrade_menu.dolomite_attack_cost,
            "dolomite_speed_level": self.upgrade_menu.dolomite_speed_level,
            "dolomite_speed_cost": self.upgrade_menu.dolomite_speed_cost,
            "marginzero_attack_level": self.upgrade_menu.marginzero_attack_level,
            "marginzero_attack_cost": self.upgrade_menu.marginzero_attack_cost,
            "marginzero_speed_level": self.upgrade_menu.marginzero_speed_level,
            "marginzero_speed_cost": self.upgrade_menu.marginzero_speed_cost,
            "max_health_level": self.upgrade_menu.max_health_level,
            "shield_capacity_level": self.upgrade_menu.shield_capacity_level,
            "shield_regen_level": self.upgrade_menu.shield_regen_level,
            "health_cost": self.upgrade_menu.health_cost,
            "shield_capacity_cost": self.upgrade_menu.shield_capacity_cost,
            "shield_regen_cost": self.upgrade_menu.shield_regen_cost
        }
        current_level = self.process.get_current_level()
        seeds_count = self.seeds_count
        ssc = self.ssc

        self.heroe = Heroe(self.screen_width // 2, self.screen_height // 2 + 50)
        self.enemy = Enemy(self.screen_width // 2, 200, level=current_level)
        self.bullets = []
        self.seeds = []
        self.airdrop_particles = []
        self.explosion_particles = []
        self.double_tap_particles = []
        self.damage_texts = []
        self.word_texts = []
        self.game_over = False
        self.double_tap_active = False
        self.double_tap_start_time = 0
        self.flash_alpha = 0
        self.current_flash_image = None
        self.current_bossback = None
        self.bossback_timer = 0
        self.attack_counter = 0
        self.next_word_attack = random.randint(4, 10)

        self.special_attacks = SpecialAttacks(self.heroe)
        for name, state in special_attacks_state.items():
            attack = self.special_attacks.attacks[name]
            attack.purchased = state["purchased"]
            attack.damage_level = state["damage_level"]
            attack.damage_cost = state["damage_cost"]
            attack.special_level = state["special_level"]
            attack.special_cost = state["special_cost"]
            attack.cooldown_time = state["cooldown_time"]
            attack.duration = state["duration"]
            attack.active = state["active"]
            attack.active_start_time = state["active_start_time"]

        self.allies = []
        for ally_state in saved_allies:
            ally = Ally(ally_state["x"], ally_state["y"], ally_type=ally_state["ally_type"])
            ally.attack_power = ally_state["attack_power"]
            ally.attack_speed = ally_state["attack_speed"]
            ally.attack_interval = ally_state["attack_interval"]
            self.allies.append(ally)

        self.seedfi_purchased = saved_purchases["seedfi_purchased"]
        self.bebop_purchased = saved_purchases["bebop_purchased"]
        self.stryke_purchased = saved_purchases["stryke_purchased"]
        self.velodrome_purchased = saved_purchases["velodrome_purchased"]
        self.ionic_purchased = saved_purchases["ionic_purchased"]
        self.bulletx_purchased = saved_purchases["bulletx_purchased"]
        self.mintpad_purchased = saved_purchases["mintpad_purchased"]
        self.fractal_purchased = saved_purchases["fractal_purchased"]
        self.dolomite_purchased = saved_purchases["dolomite_purchased"]
        self.marginzero_purchased = saved_purchases["marginzero_purchased"]

        self.upgrades = Upgrades(self.heroe, self.allies)
        self.upgrades.attack_level = upgrades_state["attack_level"]
        self.upgrades.attack_cost = upgrades_state["attack_cost"]
        self.upgrades.critical_hit_level = upgrades_state["critical_hit_level"]
        self.upgrades.critical_hit_cost = upgrades_state["critical_hit_cost"]
        self.upgrades.critical_chance_level = upgrades_state["critical_chance_level"]
        self.upgrades.critical_chance_cost = upgrades_state["critical_chance_cost"]
        self.upgrades.health_level = upgrades_state["health_level"]
        self.upgrades.health_cost = upgrades_state["health_cost"]
        self.upgrades.upgrades["attack"][0]["cost"] = self.upgrades.attack_cost
        self.upgrades.upgrades["attack"][1]["cost"] = self.upgrades.critical_hit_cost
        self.upgrades.upgrades["attack"][2]["cost"] = self.upgrades.critical_chance_cost
        self.upgrades.upgrades["health"][0]["cost"] = self.upgrades.health_cost

        self.heroe.attack_power = heroe_state["attack_power"]
        self.heroe.attack_speed = heroe_state["attack_speed"]
        self.heroe.max_health = heroe_state["max_health"]
        self.heroe.health = self.heroe.max_health
        self.heroe.critical_chance = heroe_state["critical_chance"]
        self.heroe.critical_multiplier = heroe_state["critical_multiplier"]
        self.heroe.shield_capacity = heroe_state["shield_capacity"]
        self.heroe.shield = self.heroe.shield_capacity
        self.heroe.shield_regen_rate = heroe_state["shield_regen_rate"]

        self.process.current_level = current_level
        self.process.enemies_defeated = 0
        self.heroe.level = current_level
        self.seeds_count = seeds_count
        self.ssc = ssc

        self.left_platform.set_visible(self.mintpad_purchased or self.fractal_purchased)
        self.right_platform.set_visible(self.dolomite_purchased or self.marginzero_purchased)

        self.upgrade_menu = UpgradeMenu(self)
        self.upgrade_menu.airdrop_damage_level = upgrade_menu_state["airdrop_damage_level"]
        self.upgrade_menu.airdrop_damage_cost = upgrade_menu_state["airdrop_damage_cost"]
        self.upgrade_menu.airdrop_count_level = upgrade_menu_state["airdrop_count_level"]
        self.upgrade_menu.airdrop_count_cost = upgrade_menu_state["airdrop_count_cost"]
        self.upgrade_menu.double_tap_damage_level = upgrade_menu_state["double_tap_damage_level"]
        self.upgrade_menu.double_tap_damage_cost = upgrade_menu_state["double_tap_damage_cost"]
        self.upgrade_menu.double_tap_duration_level = upgrade_menu_state["double_tap_duration_level"]
        self.upgrade_menu.double_tap_duration_cost = upgrade_menu_state["double_tap_duration_cost"]
        self.upgrade_menu.yieldstorm_duration_level = upgrade_menu_state["yieldstorm_duration_level"]
        self.upgrade_menu.yieldstorm_duration_cost = upgrade_menu_state["yieldstorm_duration_cost"]
        self.upgrade_menu.yieldstorm_cooldown_level = upgrade_menu_state["yieldstorm_cooldown_level"]
        self.upgrade_menu.yieldstorm_cooldown_cost = upgrade_menu_state["yieldstorm_cooldown_cost"]
        self.upgrade_menu.seedfi_attack_level = upgrade_menu_state["seedfi_attack_level"]
        self.upgrade_menu.seedfi_attack_cost = upgrade_menu_state["seedfi_attack_cost"]
        self.upgrade_menu.seedfi_speed_level = upgrade_menu_state["seedfi_speed_level"]
        self.upgrade_menu.seedfi_speed_cost = upgrade_menu_state["seedfi_speed_cost"]
        self.upgrade_menu.bebop_attack_level = upgrade_menu_state["bebop_attack_level"]
        self.upgrade_menu.bebop_attack_cost = upgrade_menu_state["bebop_attack_cost"]
        self.upgrade_menu.bebop_speed_level = upgrade_menu_state["bebop_speed_level"]
        self.upgrade_menu.bebop_speed_cost = upgrade_menu_state["bebop_speed_cost"]
        self.upgrade_menu.stryke_attack_level = upgrade_menu_state["stryke_attack_level"]
        self.upgrade_menu.stryke_attack_cost = upgrade_menu_state["stryke_attack_cost"]
        self.upgrade_menu.stryke_speed_level = upgrade_menu_state["stryke_speed_level"]
        self.upgrade_menu.stryke_speed_cost = upgrade_menu_state["stryke_speed_cost"]
        self.upgrade_menu.velodrome_attack_level = upgrade_menu_state["velodrome_attack_level"]
        self.upgrade_menu.velodrome_attack_cost = upgrade_menu_state["velodrome_attack_cost"]
        self.upgrade_menu.velodrome_speed_level = upgrade_menu_state["velodrome_speed_level"]
        self.upgrade_menu.velodrome_speed_cost = upgrade_menu_state["velodrome_speed_cost"]
        self.upgrade_menu.ionic_attack_level = upgrade_menu_state["ionic_attack_level"]
        self.upgrade_menu.ionic_attack_cost = upgrade_menu_state["ionic_attack_cost"]
        self.upgrade_menu.ionic_speed_level = upgrade_menu_state["ionic_speed_level"]
        self.upgrade_menu.ionic_speed_cost = upgrade_menu_state["ionic_speed_cost"]
        self.upgrade_menu.bulletx_attack_level = upgrade_menu_state["bulletx_attack_level"]
        self.upgrade_menu.bulletx_attack_cost = upgrade_menu_state["bulletx_attack_cost"]
        self.upgrade_menu.bulletx_speed_level = upgrade_menu_state["bulletx_speed_level"]
        self.upgrade_menu.bulletx_speed_cost = upgrade_menu_state["bulletx_speed_cost"]
        self.upgrade_menu.mintpad_attack_level = upgrade_menu_state["mintpad_attack_level"]
        self.upgrade_menu.mintpad_attack_cost = upgrade_menu_state["mintpad_attack_cost"]
        self.upgrade_menu.mintpad_speed_level = upgrade_menu_state["mintpad_speed_level"]
        self.upgrade_menu.mintpad_speed_cost = upgrade_menu_state["mintpad_speed_cost"]
        self.upgrade_menu.fractal_attack_level = upgrade_menu_state["fractal_attack_level"]
        self.upgrade_menu.fractal_attack_cost = upgrade_menu_state["fractal_attack_cost"]
        self.upgrade_menu.fractal_speed_level = upgrade_menu_state["fractal_speed_level"]
        self.upgrade_menu.fractal_speed_cost = upgrade_menu_state["fractal_speed_cost"]
        self.upgrade_menu.dolomite_attack_level = upgrade_menu_state["dolomite_attack_level"]
        self.upgrade_menu.dolomite_attack_cost = upgrade_menu_state["dolomite_attack_cost"]
        self.upgrade_menu.dolomite_speed_level = upgrade_menu_state["dolomite_speed_level"]
        self.upgrade_menu.dolomite_speed_cost = upgrade_menu_state["dolomite_speed_cost"]
        self.upgrade_menu.marginzero_attack_level = upgrade_menu_state["marginzero_attack_level"]
        self.upgrade_menu.marginzero_attack_cost = upgrade_menu_state["marginzero_attack_cost"]
        self.upgrade_menu.marginzero_speed_level = upgrade_menu_state["marginzero_speed_level"]
        self.upgrade_menu.marginzero_speed_cost = upgrade_menu_state["marginzero_speed_cost"]
        self.upgrade_menu.max_health_level = upgrade_menu_state["max_health_level"]
        self.upgrade_menu.shield_capacity_level = upgrade_menu_state["shield_capacity_level"]
        self.upgrade_menu.shield_regen_level = upgrade_menu_state["shield_regen_level"]
        self.upgrade_menu.health_cost = upgrade_menu_state["health_cost"]
        self.upgrade_menu.shield_capacity_cost = upgrade_menu_state["shield_capacity_cost"]
        self.upgrade_menu.shield_regen_cost = upgrade_menu_state["shield_regen_cost"]

        self.special_attacks.attacks["Airdrop"].damage_level = self.upgrade_menu.airdrop_damage_level
        self.special_attacks.attacks["Airdrop"].special_level = self.upgrade_menu.airdrop_count_level
        self.special_attacks.attacks["Double Tap"].damage_level = self.upgrade_menu.double_tap_damage_level
        self.special_attacks.attacks["Double Tap"].special_level = self.upgrade_menu.double_tap_duration_level

        self.special_controls.update_circles()
        print(f"Aliados después de reiniciar: {len(self.allies)}")

    def draw_game_over(self):
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
        self.screen.blit(game_over_text, game_over_rect)
        restart_text = self.font.render("Click to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        pygame.display.flip()

    def update(self, dt):
        self.special_attacks.update()

        self.left_platform.set_visible(self.mintpad_purchased or self.fractal_purchased)
        self.right_platform.set_visible(self.dolomite_purchased or self.marginzero_purchased)

        player_damage = self.enemy.attack()
        if player_damage > 0:
            self.heroe.take_damage(player_damage)
            self.sound_manager.play("enemy_attack")  # Reproducir sonido cuando el enemigo ataca

        for ally in self.allies:
            bullet, damage = ally.attack(self.enemy.x, self.enemy.y, dt)
            if bullet:
                self.bullets.append(bullet)

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.collides_with(self.enemy):
                closest_ally = min(self.allies, key=lambda ally: (ally.x - bullet.x)**2 + (ally.y - bullet.y)**2, default=None)
                if closest_ally:
                    damage = closest_ally.attack_power
                    self.enemy.take_damage(damage)
                    self.add_damage_text(damage)
                self.bullets.remove(bullet)
            elif (bullet.x < 0 or bullet.x > self.screen_width or
                  bullet.y < 0 or bullet.y > self.screen_height):
                self.bullets.remove(bullet)

        if not self.enemy.is_alive():
            self.process.enemy_defeated()
            self.sound_manager.play("enemy_defeated")  # Sonido de enemigo derrotado
            multiplier = self.special_attacks.get_multiplier()
            if self.enemy.is_special:
                ssc_reward = self.enemy.ssc_reward * multiplier
                self.ssc += ssc_reward
                print(f"SSC obtenido: {ssc_reward} (multiplicador: {multiplier})")
            else:
                seeds_to_drop = self.calculate_seeds_to_drop(self.process.get_current_level())
                seeds_to_drop *= multiplier
                self.seeds_count += seeds_to_drop
                print(f"Seeds obtenidos: {seeds_to_drop} (multiplicador: {multiplier})")
                seeds_to_show = min(seeds_to_drop, 5)
                for _ in range(int(seeds_to_show)):
                    seed_x = self.enemy.x + random.randint(-50, 50)
                    seed_y = self.enemy.y
                    self.seeds.append(Seed(seed_x, seed_y, self.heroe.y))

            is_boss = (self.process.enemies_defeated == 8)
            self.enemy.reset(is_boss=is_boss, level=self.process.get_current_level())

            if self.process.update():
                self.heroe.level = self.process.get_current_level()
                self.sound_manager.play("level_up")  # Reproducir sonido al subir de nivel

        if self.heroe.health <= 0:
            self.game_over = True

        if self.flash_alpha > 0:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.flash_start_time
            self.flash_alpha = max(0, 255 - (255 * elapsed_time / self.flash_duration))

        for particle in self.enemy.particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["life"] -= 16
            if particle["life"] <= 0:
                self.enemy.particles.remove(particle)

        if self.enemy.is_boss:
            current_time = pygame.time.get_ticks()
            if self.current_bossback is None:
                if current_time - self.bossback_timer >= self.bossback_interval:
                    self.current_bossback = random.choice(self.bossback_images)
                    self.bossback_timer = current_time
                    self.bossback_interval = random.randint(1500, 3000)
            else:
                if current_time - self.bossback_timer >= self.bossback_duration:
                    self.current_bossback = None
                    self.bossback_timer = current_time

        for text in self.damage_texts[:]:
            text["y"] -= 1
            text["life"] -= 16
            if text["life"] <= 0:
                self.damage_texts.remove(text)

        for word in self.word_texts[:]:
            word["y"] -= 1
            word["life"] -= 16
            if word["life"] <= 0:
                self.word_texts.remove(word)

        for seed in self.seeds[:]:
            seed.update()
            if seed.should_remove():
                self.seeds.remove(seed)

        current_time = pygame.time.get_ticks()
        for particle in self.airdrop_particles[:]:
            if current_time < particle["spawn_time"]:
                continue
            particle["y"] += particle["speed"]
            particle["life"] -= 16
            if particle["y"] >= 250 or particle["life"] <= 0:
                self.explosion_particles.append({
                    "x": particle["x"],
                    "y": particle["y"],
                    "life": 200,
                    "damage": particle["damage"]
                })
                self.enemy.take_damage(particle["damage"])
                self.add_damage_text(particle["damage"])
                self.airdrop_particles.remove(particle)

        for explosion in self.explosion_particles[:]:
            explosion["life"] -= 16
            if explosion["life"] <= 0:
                self.explosion_particles.remove(explosion)

        if self.double_tap_active:
            current_time = pygame.time.get_ticks()
            double_tap_duration = self.special_attacks.attacks["Double Tap"].duration
            if current_time - self.double_tap_start_time >= double_tap_duration:
                self.double_tap_active = False
                self.heroe.attack_power /= 2
                self.special_attacks.attacks["Double Tap"].cooldown = current_time + 180000
                self.double_tap_particles.clear()
                print(f"Double Tap desactivado: ataque del héroe restaurado a {self.heroe.attack_power}")
            for particle in self.double_tap_particles[:]:
                particle["y"] -= 2
                particle["life"] -= 16
                if particle["life"] <= 0:
                    self.double_tap_particles.remove(particle)

    def calculate_seeds_to_drop(self, level):
        if level == 1:
            return 1
        elif level == 2:
            return 3
        else:
            return min(level + 1, 10)

    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.enemy.is_boss:
            bg2 = self.darkbackground2 if self.darkbackground2 else self.background2
            bg = self.darkbackground if self.darkbackground else self.background
        else:
            bg2 = self.background2
            bg = self.background

        if bg2:
            self.screen.blit(bg2, (0, 0))

        if self.enemy.is_boss and self.current_bossback:
            bossback_rect = self.current_bossback.get_rect(center=(self.enemy.x, self.enemy.y))
            self.screen.blit(self.current_bossback, bossback_rect)

        self.enemy.draw(self.screen)
        self.left_platform.draw(self.screen)
        self.right_platform.draw(self.screen)

        if bg:
            self.screen.blit(bg, (0, 0))

        for ally in self.allies:
            ally.draw(self.screen)

        self.heroe.draw(self.screen)
        self.draw_health_bar(self.screen, self.heroe.x, self.heroe.y - 60, self.heroe.health, self.heroe.max_health, (0, 255, 0), is_enemy=False)
        if self.heroe.shield_capacity > 0:
            self.draw_shield_bar(self.screen, self.heroe.x, self.heroe.y - 50, self.heroe.shield, self.heroe.shield_capacity, (0, 191, 255))

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for seed in self.seeds:
            seed.draw(self.screen)

        if self.enemy.particles:
            for particle in self.enemy.particles:
                pygame.draw.circle(self.screen, particle["color"], (int(particle["x"]), int(particle["y"])), particle["radius"])

        if self.flash_alpha > 0 and self.current_flash_image:
            flash_surface = self.current_flash_image.copy()
            flash_surface.set_alpha(int(self.flash_alpha))
            flash_x = self.enemy.x + self.flash_offset_x
            flash_y = self.enemy.y + self.flash_offset_y
            flash_rect = flash_surface.get_rect(center=(flash_x, flash_y))
            self.screen.blit(flash_surface, flash_rect)

        current_time = pygame.time.get_ticks()
        for particle in self.airdrop_particles:
            if current_time >= particle["spawn_time"]:
                self.screen.blit(self.airdrop_image, (int(particle["x"]), int(particle["y"])))
        for explosion in self.explosion_particles:
            self.screen.blit(self.explosion_image, (int(explosion["x"]), int(explosion["y"])))

        if self.double_tap_active:
            for particle in self.double_tap_particles:
                x2_text = self.damage_font.render("x2", True, (0, 255, 0))
                self.screen.blit(x2_text, (int(particle["x"]), int(particle["y"])))

        for text in self.damage_texts:
            self.screen.blit(text["text"], (text["x"], text["y"]))

        for word in self.word_texts:
            self.screen.blit(word["text"], (word["x"], word["y"]))

        self.process.draw(self.screen, self.enemy.health, self.enemy.max_health)
        self.screen.blit(self.seeds_image, (10, 10))
        seeds_count_text = self.font.render(f"{self.seeds_count:.2f}", True, (0, 0, 0))
        self.screen.blit(seeds_count_text, (50, 15))
        self.screen.blit(self.ssc_image, (10, 50))
        ssc_count_text = self.font.render(str(self.ssc), True, (0, 0, 0))
        self.screen.blit(ssc_count_text, (50, 55))

        pygame.draw.rect(self.screen, self.pause_button_color, self.pause_button_rect)
        pygame.draw.rect(self.screen, self.pause_button_border_color, self.pause_button_rect, 2)
        pause_text_rect = self.pause_button_text.get_rect(center=self.pause_button_rect.center)
        self.screen.blit(self.pause_button_text, pause_text_rect)

        self.upgrade_menu.draw()
        self.special_controls.draw()
        pygame.display.flip()

    def draw_health_bar(self, screen, x, y, health, max_health, color, is_enemy=False):
        bar_width = 100 if is_enemy else 50
        bar_height = 10
        health_ratio = health / max_health
        health_width = bar_width * health_ratio
        border_rect = pygame.Rect(x - bar_width // 2, y, bar_width, bar_height)
        health_rect = pygame.Rect(x - bar_width // 2, y, health_width, bar_height)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 1)
        pygame.draw.rect(screen, color, health_rect)

    def draw_shield_bar(self, screen, x, y, shield, shield_capacity, color):
        bar_width = 50
        bar_height = 5
        shield_ratio = shield / shield_capacity
        shield_width = bar_width * shield_ratio
        border_rect = pygame.Rect(x - bar_width // 2, y, bar_width, bar_height)
        shield_rect = pygame.Rect(x - bar_width // 2, y, shield_width, bar_height)
        pygame.draw.rect(screen, (255, 255, 255), border_rect, 1)
        pygame.draw.rect(screen, color, shield_rect)

    def trigger_airdrop(self, count):
        current_time = pygame.time.get_ticks()
        damage_per_airdrop, _ = self.special_attacks.attacks["Airdrop"].calculate_damage()
        for i in range(count):
            delay = random.uniform(0, 500)
            spawn_time = current_time + delay
            x = random.randint(self.enemy.x - 100, self.enemy.x + 100)
            y = random.randint(-100, 0)
            self.airdrop_particles.append({
                "x": x,
                "y": y,
                "life": 1000,
                "speed": random.uniform(1, 3),
                "spawn_time": spawn_time,
                "damage": damage_per_airdrop
            })
        print(f"Airdrop activado: {count} Airdrops programados con retrasos aleatorios")
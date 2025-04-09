# special_attacks.py
import pygame

class SpecialAttack:
    def __init__(self, name, base_cost, hero):
        self.name = name
        self.base_cost = base_cost
        self.hero = hero
        self.purchased = False
        self.damage_level = 1
        self.damage_cost = 10
        self.special_level = 1
        self.special_cost = 15
        self.cooldown = 0
        self.active = False  # Para manejar el estado activo
        self.active_start_time = 0  # Para rastrear el tiempo de activación

        # Configurar cooldown y duración según el ataque
        if name == "Airdrop":
            self.cooldown_time = 60000  # 1 minuto (60,000 milisegundos)
            self.duration = None  # Sin duración activa, efecto instantáneo
        elif name == "Double Tap":
            self.cooldown_time = 180000  # 3 minutos (180,000 milisegundos)
            self.duration = 30000  # 30 segundos (30,000 milisegundos)
        elif name == "Yieldstorm":
            self.cooldown_time = 300000  # 5 minutos (300,000 milisegundos)
            self.duration = 30000  # 30 segundos (30,000 milisegundos)

    def purchase(self):
        self.purchased = True

    def upgrade_damage(self):
        self.damage_level += 1
        self.damage_cost *= 1.5

    def upgrade_duration(self):
        """Mejora específica para aumentar la duración de Yieldstorm o Double Tap."""
        if (self.name == "Yieldstorm" or self.name == "Double Tap") and self.special_level <= 5:
            self.special_level += 1
            self.special_cost *= 1.5
            if self.special_level > 1:  # No aplicar en el nivel 1
                self.duration += 1000  # Aumentar duración en 1 segundo
                print(f"{self.name} duration upgraded to {self.duration/1000} seconds")

    def upgrade_cooldown(self):
        """Mejora específica para reducir el cooldown de Yieldstorm."""
        if self.name == "Yieldstorm" and self.special_level <= 5:
            self.special_level += 1
            self.special_cost *= 1.5
            if self.special_level > 1:  # No aplicar en el nivel 1
                self.cooldown_time -= 10000  # Reducir cooldown en 10 segundos
                print(f"Yieldstorm cooldown reduced to {self.cooldown_time/1000} seconds")

    def upgrade_special(self):
        """Mejora genérica para Airdrop (más airdrops)."""
        if self.name == "Airdrop":  # Solo aplica a Airdrop
            self.special_level += 1
            self.special_cost *= 1.5

    def can_activate(self):
        current_time = pygame.time.get_ticks()
        return self.purchased and current_time >= self.cooldown

    def activate(self):
        if self.can_activate():
            self.cooldown = pygame.time.get_ticks() + self.cooldown_time
            if self.name in ["Double Tap", "Yieldstorm"]:
                self.active = True
                self.active_start_time = pygame.time.get_ticks()
            damage, count = self.calculate_damage()
            return damage, count
        return 0, 0

    def update(self):
        if self.active and self.duration is not None:  # Solo para ataques con duración
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.active_start_time
            if elapsed >= self.duration:
                self.active = False
                print(f"{self.name} desactivado después de {self.duration/1000} segundos")

    def calculate_damage(self):
        if self.name == "Airdrop":
            base_damage = 30
            damage = base_damage * (1.5 ** (min(self.damage_level, 6) - 1))  # Límite en nivel 6
            count = min(self.special_level, 5)  # Máximo 5 Airdrops
            return damage, count
        elif self.name == "Double Tap":
            return self.hero.attack_power * 1.0 * self.damage_level, 2
        elif self.name == "Yieldstorm":
            # Yieldstorm no causa daño directo, solo multiplica recompensas
            return 0, 0
        return 0, 0

class SpecialAttacks:
    def __init__(self, hero):
        self.hero = hero
        self.attacks = {
            "Airdrop": SpecialAttack("Airdrop", 50, hero),
            "Double Tap": SpecialAttack("Double Tap", 50, hero),
            "Yieldstorm": SpecialAttack("Yieldstorm", 50, hero)
        }

    def update(self):
        for attack in self.attacks.values():
            attack.update()

    def get_multiplier(self):
        # Retorna el multiplicador de recompensas si Yieldstorm está activo
        yieldstorm = self.attacks.get("Yieldstorm")
        if yieldstorm and yieldstorm.active:
            return 2.0  # Multiplicador de x2
        return 1.0

    def get_upgrades(self):
        upgrades = []
        for name, attack in self.attacks.items():
            if not attack.purchased:
                upgrades.append({
                    "name": f"Buy {name}",
                    "cost": attack.base_cost,
                    "apply": lambda a=attack: a.purchase()
                })
            else:
                upgrades.append({
                    "name": f"Upgrade {name} Damage",
                    "cost": attack.damage_cost,
                    "apply": lambda a=attack: a.upgrade_damage()
                })
                if name == "Airdrop":
                    upgrades.append({
                        "name": "More Parachutes",
                        "cost": attack.special_cost,
                        "apply": lambda a=attack: a.upgrade_special()
                    })
                elif name == "Double Tap":
                    upgrades.append({
                        "name": "Longer Duration",
                        "cost": attack.special_cost,
                        "apply": lambda a=attack: a.upgrade_duration()
                    })
                elif name == "Yieldstorm":
                    upgrades.append({
                        "name": "Yieldstorm Duration",
                        "cost": attack.special_cost,
                        "apply": lambda a=attack: a.upgrade_duration()
                    })
                    upgrades.append({
                        "name": "Yieldstorm Cooldown",
                        "cost": attack.special_cost,
                        "apply": lambda a=attack: a.upgrade_cooldown()
                    })
        return upgrades
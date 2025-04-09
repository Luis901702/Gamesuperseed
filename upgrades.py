# upgrades.py
class Upgrades:
    def __init__(self, heroe, allies):
        self.heroe = heroe
        self.allies = allies
        
        # Niveles iniciales de las mejoras
        self.attack_level = 0
        self.critical_hit_level = 0
        self.critical_chance_level = 0
        self.health_level = 0
        
        # Costos iniciales
        self.attack_cost = 10
        self.critical_hit_cost = 20
        self.critical_chance_cost = 15
        self.health_cost = 10
        
        # Diccionario de mejoras disponibles
        self.upgrades = {
            "attack": [
                {"name": "Increase Attack", "cost": self.attack_cost},
                {"name": "Critical Hit", "cost": self.critical_hit_cost},
                {"name": "Critical Chance", "cost": self.critical_chance_cost}
            ],
            "health": [
                {"name": "Increase Health", "cost": self.health_cost}
            ]
        }

    def apply_upgrade(self, category, upgrade_name):
        if category == "attack":
            if upgrade_name == "Increase Attack" and self.attack_level < 10:
                self.attack_level += 1
                self.heroe.attack_power += 15  # Incremento de 15 por nivel
                self.attack_cost = int(self.attack_cost * 1.5)
                self.upgrades["attack"][0]["cost"] = self.attack_cost
                print(f"Ataque mejorado al nivel {self.attack_level}. Nuevo poder de ataque: {self.heroe.attack_power}")
            
            elif upgrade_name == "Critical Hit" and self.critical_hit_level < 5:
                self.critical_hit_level += 1
                self.heroe.critical_multiplier = 1.2 + (self.critical_hit_level - 1) * 0.15  # 120% + 15% por nivel
                self.critical_hit_cost = int(self.critical_hit_cost * 1.5)
                self.upgrades["attack"][1]["cost"] = self.critical_hit_cost
                print(f"Golpe Crítico mejorado al nivel {self.critical_hit_level}. Multiplicador: {self.heroe.critical_multiplier}")
            
            elif upgrade_name == "Critical Chance" and self.critical_chance_level < 10:
                self.critical_chance_level += 1
                self.heroe.critical_chance = 0.01 + (self.critical_chance_level - 1) * 0.01  # 1% + 1% por nivel
                self.critical_chance_cost = int(self.critical_chance_cost * 1.5)
                self.upgrades["attack"][2]["cost"] = self.critical_chance_cost
                print(f"Probabilidad Crítica mejorada al nivel {self.critical_chance_level}. Probabilidad: {self.heroe.critical_chance*100}%")
        
        elif category == "health" and upgrade_name == "Increase Health":
            self.health_level += 1
            self.heroe.max_health += 20
            self.heroe.health = self.heroe.max_health
            self.health_cost += 10
            self.upgrades["health"][0]["cost"] = self.health_cost
            print(f"Salud mejorada al nivel {self.health_level}. Nueva salud máxima: {self.heroe.max_health}")

    def get_attack_level(self):
        return self.attack_level

    def get_critical_hit_level(self):
        return self.critical_hit_level

    def get_critical_chance_level(self):
        return self.critical_chance_level

    def get_health_level(self):
        return self.health_level

    def get_attack_cost(self):
        return self.attack_cost

    def get_critical_hit_cost(self):
        return self.critical_hit_cost

    def get_critical_chance_cost(self):
        return self.critical_chance_cost

    def get_health_cost(self):
        return self.health_cost